import React from 'react';
import { CELL_VALUES } from '../../utils/constants';
import './GameBoard.css';

const Cell = ({ value, row, col, onClick, isValid, isHighlighted, isGiven }) => {
  const handleClick = () => {
    onClick(row, col);
  };

  const getCellClass = () => {
    let classes = ['cell'];
    if (value === CELL_VALUES.SUN) classes.push('sun');
    if (value === CELL_VALUES.MOON) classes.push('moon');
    if (!isValid) classes.push('invalid');
    if (isHighlighted) classes.push('highlighted');
    if (isGiven) classes.push('given');
    return classes.join(' ');
  };

  const getCellContent = () => {
    if (value === CELL_VALUES.SUN) return '☀️';
    if (value === CELL_VALUES.MOON) return '🌙';
    return '';
  };

  return (
    <div 
      className={getCellClass()} 
      onClick={handleClick}
      data-row={row}
      data-col={col}
    >
      {getCellContent()}
    </div>
  );
};

export default Cell;