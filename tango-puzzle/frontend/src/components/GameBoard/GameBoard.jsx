import React from 'react';
import Cell from './Cell';
import Constraint from './Constraint';
import { GRID_SIZE } from '../../utils/constants';
import './GameBoard.css';

const GameBoard = ({ 
  grid, 
  constraints, 
  onCellClick, 
  validationErrors = [],
  highlightedCells = [],
  initialGrid = null,
  validationDetails = null,
  onErrorInfoClick
}) => {
  const isValidCell = (row, col) => {
    return !validationErrors.some(error => 
      error.row === row && error.col === col
    );
  };

  const isHighlightedCell = (row, col) => {
    return highlightedCells.some(cell => 
      cell.row === row && cell.col === col
    );
  };

  // Parse validation details to get errors by row and column
  const getRowErrors = (rowIndex) => {
    if (!validationDetails || !validationDetails.errors) return [];
    return validationDetails.errors.filter(error => 
      (error.type === 'row_count' || error.type === 'row_balance' || error.type === 'row_consecutive') && 
      error.row === rowIndex
    );
  };

  const getColumnErrors = (colIndex) => {
    if (!validationDetails || !validationDetails.errors) return [];
    return validationDetails.errors.filter(error => 
      (error.type === 'column_count' || error.type === 'column_balance' || error.type === 'column_consecutive') && 
      error.col === colIndex
    );
  };

  return (
    <div className="game-board-wrapper">
      <div className="game-board-container">
        {/* Column numbers */}
        <div className="board-numbers-top">
          {Array.from({ length: GRID_SIZE }, (_, i) => (
            <div key={`col-num-${i}`} className="board-number">
              {i + 1}
            </div>
          ))}
        </div>
        
        {/* Row numbers */}
        <div className="board-numbers-left">
          {Array.from({ length: GRID_SIZE }, (_, i) => (
            <div key={`row-num-${i}`} className="board-number">
              {i + 1}
            </div>
          ))}
        </div>
        
        <div className="game-board">
          {/* Render cells */}
          {grid.map((row, rowIndex) => (
            row.map((cell, colIndex) => (
              <Cell
                key={`${rowIndex}-${colIndex}`}
                value={cell}
                row={rowIndex}
                col={colIndex}
                onClick={onCellClick}
                isValid={isValidCell(rowIndex, colIndex)}
                isHighlighted={isHighlightedCell(rowIndex, colIndex)}
                isGiven={initialGrid && initialGrid[rowIndex][colIndex] !== null}
              />
            ))
          ))}
        
        {/* Render constraints */}
        {constraints.map((constraint, index) => (
          <Constraint
            key={index}
            type={constraint.type}
            position={{
              row1: constraint.row1,
              col1: constraint.col1,
              row2: constraint.row2,
              col2: constraint.col2
            }}
          />
        ))}
        </div>
        
        {/* Single error indicator in upper right */}
        {validationDetails && validationDetails.errors && validationDetails.errors.length > 0 && (
          <button 
            className="error-info-button-main"
            onClick={() => onErrorInfoClick('all', 0, validationDetails.errors)}
            title="View validation errors"
          >
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <circle cx="10" cy="10" r="9" stroke="currentColor" strokeWidth="2"/>
              <path d="M10 6V11" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
              <circle cx="10" cy="14" r="1" fill="currentColor"/>
            </svg>
          </button>
        )}
      </div>
    </div>
  );
};

export default GameBoard;