import React from 'react';
import './GameBoard.css';

const ErrorInfo = ({ type, index, errors, onClick }) => {
  const hasErrors = errors && errors.length > 0;
  
  if (!hasErrors) return null;
  
  const handleClick = (e) => {
    e.preventDefault();
    onClick(type, index, errors);
  };
  
  return (
    <button 
      className={`error-info-button ${type}`}
      onClick={handleClick}
      title="Click for error details"
    >
      i
    </button>
  );
};

export default ErrorInfo;