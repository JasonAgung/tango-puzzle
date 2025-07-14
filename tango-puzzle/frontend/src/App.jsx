import React, { useState, useEffect } from 'react';
import GameBoard from './components/GameBoard/GameBoard';
import Controls from './components/Controls/Controls';
import Modal from './components/UI/Modal';
import { GRID_SIZE, CELL_VALUES, DIFFICULTIES } from './utils/constants';
import { useGameState } from './hooks/useGameState';
import { useTimer } from './hooks/useTimer';
import { puzzleAPI, solverAPI } from './services/api';
import './App.css';

function App() {
  const {
    grid,
    constraints,
    difficulty,
    moveCount,
    isComplete,
    setGrid,
    setConstraints,
    setDifficulty,
    setIsComplete,
    incrementMoves,
    checkCompletion,
    resetGame
  } = useGameState();

  const { timeElapsed, startTimer, stopTimer, resetTimer } = useTimer();
  const [validationErrors, setValidationErrors] = useState([]);
  const [highlightedCells, setHighlightedCells] = useState([]);
  const [currentPuzzleId, setCurrentPuzzleId] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showHowToPlay, setShowHowToPlay] = useState(false);
  const [message, setMessage] = useState('');
  const [moveHistory, setMoveHistory] = useState([]);
  const [redoHistory, setRedoHistory] = useState([]);
  const [darkMode, setDarkMode] = useState(() => {
    // Check localStorage for saved preference
    return localStorage.getItem('darkMode') === 'true';
  });
  const [initialGrid, setInitialGrid] = useState(null);
  const [validationDetails, setValidationDetails] = useState(null);
  const [showErrorInfo, setShowErrorInfo] = useState(null);
  const [showHintInfo, setShowHintInfo] = useState(null);

  // Start timer when game starts
  useEffect(() => {
    if (!isComplete && moveCount > 0) {
      startTimer();
    } else if (isComplete) {
      stopTimer();
    }
  }, [isComplete, moveCount, startTimer, stopTimer]);

  // Apply dark mode class to body
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode');
    } else {
      document.body.classList.remove('dark-mode');
    }
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(prev => !prev);
  };

  const handleErrorInfoClick = (type, index, errors) => {
    if (type === 'all') {
      // Format all errors with proper indexing
      const formattedErrors = errors.map(error => {
        // Adjust the message to use 1-based indexing for display
        let message = error.message;
        
        // Replace all row/column references (both uppercase and lowercase)
        // Handle "Row X", "row X", "Column X", "column X" patterns
        message = message.replace(/\b[Rr]ow (\d+)/g, (match, num) => {
          const rowNum = parseInt(num) + 1;
          return match.charAt(0) === 'R' ? `Row ${rowNum}` : `row ${rowNum}`;
        });
        
        message = message.replace(/\b[Cc]olumn (\d+)/g, (match, num) => {
          const colNum = parseInt(num) + 1;
          return match.charAt(0) === 'C' ? `Column ${colNum}` : `column ${colNum}`;
        });
        
        return message;
      }).join('\n');
      
      setShowErrorInfo({ 
        location: '❌ Validation Errors', 
        messages: formattedErrors 
      });
    }
  };

  // Load initial puzzle on mount
  useEffect(() => {
    handleNewGame();
  }, []);

  const handleCellClick = async (row, col) => {
    if (isComplete || loading) return;
    
    // Check if this is an initial cell (given by the puzzle)
    if (initialGrid && initialGrid[row][col] !== null) {
      return;
    }

    const newGrid = [...grid];
    const currentValue = newGrid[row][col];
    const previousValue = currentValue;

    // Cycle through values: empty -> sun -> moon -> empty
    if (currentValue === null) {
      newGrid[row][col] = CELL_VALUES.SUN;
    } else if (currentValue === CELL_VALUES.SUN) {
      newGrid[row][col] = CELL_VALUES.MOON;
    } else {
      newGrid[row][col] = null;
    }

    // Add to history for undo functionality
    setMoveHistory(prev => [...prev, { row, col, previousValue, newValue: newGrid[row][col] }]);
    
    // Clear redo history when making a new move
    setRedoHistory([]);
    
    setGrid(newGrid);
    incrementMoves();
    
    // Validate with backend if we have a puzzle ID
    if (currentPuzzleId) {
      try {
        const validation = await puzzleAPI.validate(currentPuzzleId, newGrid);
        
        if (!validation.valid) {
          // Convert invalid cells to the format expected by GameBoard
          const errors = validation.invalid_cells.map(([row, col]) => ({ row, col }));
          setValidationErrors(errors);
          // Store full validation details for error display
          setValidationDetails(validation);
        } else {
          setValidationErrors([]);
          setValidationDetails(null);
        }
        
        if (validation.complete) {
          setIsComplete(true);
        }
      } catch (error) {
        console.error('Validation error:', error);
      }
    } else {
      // Local validation only
      checkCompletion(newGrid);
    }
  };

  const handleNewGame = async () => {
    setLoading(true);
    try {
      // Fetch new puzzle from backend
      const puzzleData = await puzzleAPI.generate(difficulty);
      
      setCurrentPuzzleId(puzzleData.id);
      setGrid(puzzleData.grid);
      setInitialGrid(puzzleData.grid.map(row => [...row])); // Deep copy
      setConstraints(puzzleData.constraints);
      resetGame();
      resetTimer();
      setValidationErrors([]);
      setHighlightedCells([]);
      setMoveHistory([]);
      setRedoHistory([]);
    } catch (error) {
      console.error('Error generating puzzle:', error);
      // Fallback to empty grid
      const emptyGrid = Array(GRID_SIZE).fill(null).map(() => Array(GRID_SIZE).fill(null));
      setGrid(emptyGrid);
      setConstraints([]);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    if (currentPuzzleId) {
      try {
        // Fetch original puzzle
        const puzzleData = await puzzleAPI.get(currentPuzzleId);
        setGrid(puzzleData.grid);
        resetGame();
        resetTimer();
        setValidationErrors([]);
        setHighlightedCells([]);
        setMoveHistory([]);
        setRedoHistory([]);
        setValidationDetails(null);
      } catch (error) {
        console.error('Error resetting puzzle:', error);
      }
    } else {
      const emptyGrid = Array(GRID_SIZE).fill(null).map(() => Array(GRID_SIZE).fill(null));
      setGrid(emptyGrid);
      resetGame();
      resetTimer();
      setValidationErrors([]);
    }
  };

  const handleUndo = async () => {
    if (moveHistory.length === 0) return;
    
    const lastMove = moveHistory[moveHistory.length - 1];
    const newGrid = [...grid];
    
    // Restore previous value
    newGrid[lastMove.row][lastMove.col] = lastMove.previousValue;
    
    // Add to redo history
    setRedoHistory(prev => [...prev, lastMove]);
    
    // Remove last move from history
    setMoveHistory(prev => prev.slice(0, -1));
    
    setGrid(newGrid);
    
    // Validate the new state
    if (currentPuzzleId) {
      try {
        const validation = await puzzleAPI.validate(currentPuzzleId, newGrid);
        
        if (!validation.valid) {
          const errors = validation.invalid_cells.map(([row, col]) => ({ row, col }));
          setValidationErrors(errors);
          setValidationDetails(validation);
        } else {
          setValidationErrors([]);
          setValidationDetails(null);
        }
      } catch (error) {
        console.error('Validation error:', error);
      }
    }
  };

  const handleRedo = async () => {
    if (redoHistory.length === 0) return;
    
    const moveToRedo = redoHistory[redoHistory.length - 1];
    const newGrid = [...grid];
    
    // Apply the move again
    newGrid[moveToRedo.row][moveToRedo.col] = moveToRedo.newValue;
    
    // Add back to move history
    setMoveHistory(prev => [...prev, moveToRedo]);
    
    // Remove from redo history
    setRedoHistory(prev => prev.slice(0, -1));
    
    setGrid(newGrid);
    
    // Validate the new state
    if (currentPuzzleId) {
      try {
        const validation = await puzzleAPI.validate(currentPuzzleId, newGrid);
        
        if (!validation.valid) {
          const errors = validation.invalid_cells.map(([row, col]) => ({ row, col }));
          setValidationErrors(errors);
          setValidationDetails(validation);
        } else {
          setValidationErrors([]);
          setValidationDetails(null);
        }
      } catch (error) {
        console.error('Validation error:', error);
      }
    }
  };

  const handleHint = async () => {
    if (!currentPuzzleId || loading) return;
    
    // Check if there are validation errors first
    if (validationErrors.length > 0) {
      setShowHintInfo({
        noHint: true,
        message: '⚠️ Please fix the validation errors first!\n\nThe board has some rule violations that need to be corrected before hints can be provided.'
      });
      return;
    }
    
    setLoading(true);
    try {
      const hint = await solverAPI.getHint(currentPuzzleId, grid);
      
      if (hint && hint.row !== undefined && hint.col !== undefined) {
        // Highlight the hint cell
        setHighlightedCells([{ row: hint.row, col: hint.col }]);
        
        // Show hint in modal with 1-based indexing
        setShowHintInfo({
          row: hint.row + 1,
          col: hint.col + 1,
          value: hint.value,
          explanation: hint.explanation
        });
        
        // Clear highlight after 5 seconds
        setTimeout(() => {
          setHighlightedCells([]);
        }, 5000);
      } else {
        // Check if puzzle is complete
        const isGridComplete = grid.every(row => row.every(cell => cell !== null));
        
        if (isGridComplete && !isComplete) {
          setShowHintInfo({
            noHint: true,
            message: '🎯 The puzzle is fully filled!\n\nIf it\'s not marked as complete, there might be an error in the solution. Check the validation errors.'
          });
        } else if (hint?.error && hint.error.includes('unsolvable')) {
          // Puzzle is in an unsolvable state
          setShowHintInfo({
            noHint: true,
            message: '🤔 The current board state might lead to an unsolvable puzzle.\n\nEven though no rules are broken yet, the current configuration may prevent a valid solution.\n\nTry undoing some recent moves or reset to start fresh.'
          });
        } else {
          // No hint available - show message in modal
          setShowHintInfo({
            noHint: true,
            message: '💭 No hints available at this moment.\n\nTry filling in a few more cells using logical deduction based on the rules.'
          });
        }
      }
    } catch (error) {
      // Check if it's an unsolvable state error (not a real error, just a state)
      if (error.response?.data?.detail && 
          (error.response.data.detail.includes('unsolvable') || 
           error.response.data.detail.includes('No hint available'))) {
        setShowHintInfo({
          noHint: true,
          message: '🤔 The current board state might lead to an unsolvable puzzle.\n\nEven though no rules are broken yet, the current configuration may prevent a valid solution.\n\nTry undoing some recent moves or reset to start fresh.'
        });
      } else {
        // Log other errors but don't show the raw error message
        console.error('Error getting hint:', error);
        // Show generic error in modal
        setShowHintInfo({
          noHint: true,
          message: '❌ Unable to generate hint.\n\nPlease try again in a moment.'
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSolve = async () => {
    if (!currentPuzzleId || loading) return;
    
    setLoading(true);
    try {
      // First, get the original puzzle to solve from scratch
      const puzzleData = await puzzleAPI.get(currentPuzzleId);
      
      // Solve from the initial state (not current state)
      const solution = await solverAPI.solve(currentPuzzleId, puzzleData.grid);
      
      // Show solution
      setGrid(solution.solution);
      setValidationErrors([]);
      setValidationDetails(null);
      setIsComplete(true);
      
      // Clear move history since we're showing the solution
      setMoveHistory([]);
      setRedoHistory([]);
      
      // Optional: Show solution steps
      console.log('Solution steps:', solution.steps);
    } catch (error) {
      console.error('Error solving puzzle:', error);
      // If still can't solve, show error message
      setMessage('Unable to show solution. Please try generating a new puzzle.');
      setTimeout(() => setMessage(''), 3000);
    } finally {
      setLoading(false);
    }
  };


  const handleDifficultyChange = async (newDifficulty) => {
    console.log('Difficulty change requested:', newDifficulty);
    setLoading(true);
    setDifficulty(newDifficulty);
    // Use newDifficulty directly since state hasn't updated yet
    try {
      const puzzleData = await puzzleAPI.generate(newDifficulty);
      console.log('Received puzzle data:', puzzleData);
      
      setCurrentPuzzleId(puzzleData.id);
      setGrid(puzzleData.grid);
      setInitialGrid(puzzleData.grid.map(row => [...row])); // Deep copy
      setConstraints(puzzleData.constraints);
      resetGame();
      resetTimer();
      setValidationErrors([]);
      setHighlightedCells([]);
      setMoveHistory([]);
      setRedoHistory([]);
      setMessage('');
    } catch (error) {
      console.error('Error generating puzzle:', error);
      setMessage('Failed to generate puzzle. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="title-section">
            <h1 className="game-title">
              <span className="title-icon">🎯</span>
              Tango Puzzle
            </h1>
            <p className="game-subtitle">Fill the grid with suns and moons following the rules!</p>
          </div>
          <button 
            className="dark-mode-toggle" 
            onClick={toggleDarkMode}
            title={darkMode ? "Switch to light mode" : "Switch to dark mode"}
          >
            {darkMode ? '☀️' : '🌙'}
          </button>
        </div>
      </header>
      
      <main className="app-main">
        <div className="game-area">
          {loading && (
            <div className="loading-overlay">
              <div className="loading-spinner">Loading...</div>
            </div>
          )}
          {message && (
            <div className="message-banner">
              {message}
            </div>
          )}
          <GameBoard
            grid={grid}
            constraints={constraints}
            onCellClick={handleCellClick}
            validationErrors={validationErrors}
            highlightedCells={highlightedCells}
            initialGrid={initialGrid}
            validationDetails={validationDetails}
            onErrorInfoClick={handleErrorInfoClick}
          />
          
          <div className="board-controls">
            <button 
              className="board-control-button" 
              onClick={handleUndo}
              disabled={moveHistory.length === 0}
              title="Undo"
            >
              ← Undo
            </button>
            
            <button 
              className="board-control-button reset" 
              onClick={handleReset}
              disabled={moveCount === 0}
              title="Reset"
            >
              Reset
            </button>
            
            <button 
              className="board-control-button" 
              onClick={handleRedo}
              disabled={redoHistory.length === 0}
              title="Redo"
            >
              Redo →
            </button>
          </div>
        </div>
        
        <aside className="controls-area">
          <Controls
            difficulty={difficulty}
            onDifficultyChange={handleDifficultyChange}
            onNewGame={handleNewGame}
            onHint={handleHint}
            onSolve={handleSolve}
            timeElapsed={timeElapsed}
            moveCount={moveCount}
            isGameComplete={isComplete}
          />
        </aside>
      </main>
      
      <footer className="app-footer">
        <button 
          className="how-to-play-button" 
          onClick={() => setShowHowToPlay(true)}
        >
          How to Play
        </button>
      </footer>

      {showErrorInfo && (
        <Modal onClose={() => setShowErrorInfo(null)}>
          <div className="error-info-content">
            <h2>{showErrorInfo.location}</h2>
            <p>{showErrorInfo.messages}</p>
          </div>
        </Modal>
      )}

      {showHintInfo && (
        <Modal onClose={() => setShowHintInfo(null)}>
          <div className="hint-info-content">
            <h2>💡 Hint</h2>
            {showHintInfo.noHint ? (
              <p className="hint-no-available">{showHintInfo.message}</p>
            ) : (
              <>
                <p className="hint-location">Row {showHintInfo.row}, Column {showHintInfo.col}</p>
                <p className="hint-value">Should be: <strong>{showHintInfo.value === 'sun' ? '☀️ Sun' : '🌙 Moon'}</strong></p>
                <p className="hint-explanation">{showHintInfo.explanation}</p>
              </>
            )}
          </div>
        </Modal>
      )}


      {showHowToPlay && (
        <Modal onClose={() => setShowHowToPlay(false)}>
          <div className="how-to-play-content">
            <h2>How to Play Tango Puzzle</h2>
            
            <h3>Objective</h3>
            <p>Fill the 6×6 grid with suns ☀️ and moons 🌙 following the rules below.</p>
            
            <h3>Rules</h3>
            <ol>
              <li><strong>Equal Distribution:</strong> Each row and column must contain exactly 3 suns and 3 moons.</li>
              <li><strong>No Three in a Row:</strong> You cannot place more than 2 consecutive identical symbols horizontally or vertically.</li>
              <li><strong>Equal Constraint (=):</strong> Cells connected by an equals sign must contain the same symbol.</li>
              <li><strong>Opposite Constraint (×):</strong> Cells connected by a cross sign must contain opposite symbols.</li>
            </ol>
            
            <h3>How to Play</h3>
            <ul>
              <li>Click on an empty cell to cycle through: empty → sun → moon → empty</li>
              <li>Use the <strong>Check</strong> button to verify your solution</li>
              <li>Use the <strong>Hint</strong> button when you're stuck</li>
              <li>Use the <strong>Solve</strong> button to see the complete solution</li>
            </ul>
            
            <h3>Tips</h3>
            <ul>
              <li>Start with rows or columns that already have 2 of the same symbol</li>
              <li>Look for constraint symbols (= and ×) to deduce connected cells</li>
              <li>Check for potential three-in-a-row violations</li>
              <li>Each puzzle has exactly one unique solution</li>
            </ul>
          </div>
        </Modal>
      )}
    </div>
  );
}

export default App;