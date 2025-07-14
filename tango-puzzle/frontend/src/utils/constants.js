export const GRID_SIZE = 6;

export const CELL_VALUES = {
  EMPTY: null,
  SUN: 'sun',
  MOON: 'moon'
};

export const CONSTRAINT_TYPES = {
  EQUAL: 'equal',
  OPPOSITE: 'opposite'
};

export const DIFFICULTIES = {
  EASY: 'easy',
  MEDIUM: 'medium',
  HARD: 'hard'
};

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';