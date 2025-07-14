import React from 'react';
import DifficultySelector from './DifficultySelector';
import GameTimer from './GameTimer';
import './Controls.css';

const Controls = ({ 
  difficulty, 
  onDifficultyChange, 
  onNewGame, 
  onHint,
  onSolve,
  timeElapsed,
  moveCount,
  isGameComplete
}) => {
  return (
    <div className="controls-container">
      <div className="controls-section">
        <h3>Game Controls</h3>
        
        <DifficultySelector 
          difficulty={difficulty} 
          onDifficultyChange={onDifficultyChange} 
        />
        
        <div className="button-group">
          <button 
            className="control-button primary" 
            onClick={onNewGame}
          >
            New Game
          </button>
        </div>
        
        <div className="button-group">
          <button 
            className="control-button hint" 
            onClick={onHint}
            disabled={isGameComplete}
          >
            Hint
          </button>
          
          <button 
            className="control-button solve" 
            onClick={onSolve}
            disabled={isGameComplete}
          >
            Show Solution
          </button>
        </div>
      </div>
      
      <div className="controls-section">
        <h3>Game Stats</h3>
        <GameTimer timeElapsed={timeElapsed} />
        <div className="stat-item">
          <span className="stat-label">Moves:</span>
          <span className="stat-value">{moveCount}</span>
        </div>
        {isGameComplete && (
          <div className="completion-message">
            🎉 Puzzle Completed! 🎉
          </div>
        )}
      </div>
    </div>
  );
};

export default Controls;