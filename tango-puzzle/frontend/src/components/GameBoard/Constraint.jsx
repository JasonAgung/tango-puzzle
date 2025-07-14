import React from 'react';
import { CONSTRAINT_TYPES } from '../../utils/constants';
import './GameBoard.css';

const Constraint = ({ type, position }) => {
  const getConstraintSymbol = () => {
    return type === CONSTRAINT_TYPES.EQUAL ? '=' : '×';
  };

  const getPositionStyle = () => {
    const { row1, col1, row2, col2 } = position;
    const cellSize = 60; // Match the CSS cell size
    
    // Horizontal constraint (between left and right cells)
    if (row1 === row2 && Math.abs(col1 - col2) === 1) {
      const row = row1;
      const leftCol = Math.min(col1, col2);
      
      return {
        position: 'absolute',
        top: `${row * cellSize + cellSize / 2 - 15}px`, // Center vertically
        left: `${(leftCol + 1) * cellSize - 15}px`, // Between cells
        width: '30px',
        height: '30px',
      };
    }
    
    // Vertical constraint (between top and bottom cells)
    if (col1 === col2 && Math.abs(row1 - row2) === 1) {
      const col = col1;
      const topRow = Math.min(row1, row2);
      
      return {
        position: 'absolute',
        top: `${(topRow + 1) * cellSize - 15}px`, // Between cells
        left: `${col * cellSize + cellSize / 2 - 15}px`, // Center horizontally
        width: '30px',
        height: '30px',
      };
    }
    
    // Invalid constraint position
    return { display: 'none' };
  };

  const getOrientationClass = () => {
    const { row1, row2 } = position;
    return row1 === row2 ? 'horizontal' : 'vertical';
  };

  return (
    <div 
      className={`constraint ${getOrientationClass()}`}
      style={getPositionStyle()}
    >
      {getConstraintSymbol()}
    </div>
  );
};

export default Constraint;