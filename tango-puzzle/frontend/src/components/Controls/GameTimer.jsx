import React from 'react';

const GameTimer = ({ timeElapsed }) => {
  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="game-timer">
      <span className="stat-label">Time:</span>
      <span className="stat-value">{formatTime(timeElapsed)}</span>
    </div>
  );
};

export default GameTimer;