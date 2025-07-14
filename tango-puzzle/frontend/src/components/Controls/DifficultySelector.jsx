import React from 'react';
import { DIFFICULTIES } from '../../utils/constants';

const DifficultySelector = ({ difficulty, onDifficultyChange }) => {
  return (
    <div className="difficulty-selector">
      <label htmlFor="difficulty">Difficulty:</label>
      <select 
        id="difficulty"
        value={difficulty} 
        onChange={(e) => onDifficultyChange(e.target.value)}
        className="difficulty-select"
      >
        <option value={DIFFICULTIES.EASY}>Easy</option>
        <option value={DIFFICULTIES.MEDIUM}>Medium</option>
        <option value={DIFFICULTIES.HARD}>Hard</option>
      </select>
    </div>
  );
};

export default DifficultySelector;