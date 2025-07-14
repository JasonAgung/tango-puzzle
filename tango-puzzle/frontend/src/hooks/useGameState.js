import { useState } from 'react';
import { GRID_SIZE, DIFFICULTIES } from '../utils/constants';

export const useGameState = () => {
  const [grid, setGrid] = useState(() => 
    Array(GRID_SIZE).fill(null).map(() => Array(GRID_SIZE).fill(null))
  );
  const [constraints, setConstraints] = useState([]);
  const [difficulty, setDifficulty] = useState(DIFFICULTIES.MEDIUM);
  const [moveCount, setMoveCount] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  const incrementMoves = () => {
    setMoveCount(prev => prev + 1);
  };

  const resetGame = () => {
    setMoveCount(0);
    setIsComplete(false);
  };

  const checkCompletion = (currentGrid) => {
    // Check if all cells are filled
    const allFilled = currentGrid.every(row => 
      row.every(cell => cell !== null)
    );

    if (!allFilled) {
      setIsComplete(false);
      return false;
    }

    // TODO: Add validation logic here
    // For now, just mark as complete if all cells are filled
    setIsComplete(true);
    return true;
  };

  return {
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
  };
};