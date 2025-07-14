import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Puzzle API
export const puzzleAPI = {
  // Generate a new puzzle
  generate: async (difficulty) => {
    const response = await api.post('/puzzle/generate', { difficulty });
    return response.data;
  },

  // Get a specific puzzle
  get: async (puzzleId) => {
    const response = await api.get(`/puzzle/${puzzleId}`);
    return response.data;
  },

  // Validate current board state
  validate: async (puzzleId, grid) => {
    const response = await api.post('/puzzle/validate', {
      puzzle_id: puzzleId,
      grid: grid
    });
    return response.data;
  },
};

// Solver API
export const solverAPI = {
  // Get complete solution
  solve: async (puzzleId, currentGrid) => {
    const response = await api.post('/solver/solve', {
      puzzle_id: puzzleId,
      current_grid: currentGrid
    });
    return response.data;
  },

  // Get hint for next move
  getHint: async (puzzleId, currentGrid) => {
    const response = await api.post('/solver/hint', {
      puzzle_id: puzzleId,
      current_grid: currentGrid
    });
    return response.data;
  },

  // Get step-by-step explanation
  getExplanation: async (puzzleId, currentGrid) => {
    const response = await api.post('/solver/explain', {
      puzzle_id: puzzleId,
      current_grid: currentGrid
    });
    return response.data;
  },

  // Check if puzzle is solvable
  checkSolvability: async (puzzleId, currentGrid) => {
    const response = await api.post('/solver/check', {
      puzzle_id: puzzleId,
      current_grid: currentGrid
    });
    return response.data;
  },
};

// Game API
export const gameAPI = {
  // Save game state
  save: async (puzzleId, grid, timeElapsed, movesCount) => {
    const response = await api.post('/game/save', {
      puzzle_id: puzzleId,
      grid: grid,
      time_elapsed: timeElapsed,
      moves_count: movesCount
    });
    return response.data;
  },

  // Load game state
  load: async (saveId) => {
    const response = await api.get(`/game/load/${saveId}`);
    return response.data;
  },
};

// Error interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error status
      const message = error.response.data.detail || 'An error occurred';
      
      // Don't show alert for expected hint/solver errors
      const isExpectedError = message.includes('No hint available') || 
                             message.includes('unsolvable') ||
                             message.includes('cannot be solved');
      
      if (!isExpectedError) {
        console.error('API Error:', error.response.data);
        alert(`Error: ${message}`);
      }
    } else if (error.request) {
      // Request was made but no response
      console.error('No response from server');
      alert('Unable to connect to server. Please check your connection.');
    } else {
      // Something else happened
      console.error('Error:', error.message);
      alert('An unexpected error occurred');
    }
    
    return Promise.reject(error);
  }
);

export default api;