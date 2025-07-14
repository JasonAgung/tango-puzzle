from fastapi import APIRouter, HTTPException
from typing import Dict, List
import uuid
from datetime import datetime
from app.api.models.puzzle import PuzzleCreate, PuzzleResponse, PuzzleValidate
from app.core.puzzle_generator import PuzzleGenerator
from app.core.constraint_validator import ConstraintValidator
from app.core.difficulty_analyzer import DifficultyAnalyzer

router = APIRouter()

# In-memory storage for puzzles (in production, use a database)
puzzle_storage = {}


@router.post("/generate", response_model=PuzzleResponse)
async def generate_puzzle(puzzle_config: PuzzleCreate):
    """Generate a new Tango puzzle with specified difficulty"""
    generator = PuzzleGenerator()
    
    # Generate puzzle
    puzzle_data = generator.generate_puzzle(puzzle_config.difficulty)
    
    # Create unique ID
    puzzle_id = str(uuid.uuid4())
    
    # Store puzzle (including solution for validation)
    puzzle_storage[puzzle_id] = {
        "puzzle_data": puzzle_data,
        "created_at": datetime.now()
    }
    
    # Return puzzle without solution
    return PuzzleResponse(
        id=puzzle_id,
        grid=puzzle_data["grid"],
        constraints=puzzle_data["constraints"],
        difficulty=puzzle_data["difficulty"],
        created_at=datetime.now()
    )


@router.get("/{puzzle_id}", response_model=PuzzleResponse)
async def get_puzzle(puzzle_id: str):
    """Get a specific puzzle by ID"""
    if puzzle_id not in puzzle_storage:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    stored_puzzle = puzzle_storage[puzzle_id]
    puzzle_data = stored_puzzle["puzzle_data"]
    
    return PuzzleResponse(
        id=puzzle_id,
        grid=puzzle_data["grid"],
        constraints=puzzle_data["constraints"],
        difficulty=puzzle_data["difficulty"],
        created_at=stored_puzzle["created_at"]
    )


@router.post("/validate")
async def validate_puzzle_state(validation_request: PuzzleValidate):
    """Validate current board state"""
    validator = ConstraintValidator()
    
    # Get stored puzzle to access constraints
    if validation_request.puzzle_id in puzzle_storage:
        constraints = puzzle_storage[validation_request.puzzle_id]["puzzle_data"]["constraints"]
    else:
        constraints = []
    
    # Validate the grid
    validation_result = validator.validate_grid(validation_request.grid, constraints)
    
    return {
        "valid": validation_result["valid"],
        "complete": validation_result["complete"],
        "errors": validation_result["errors"],
        "invalid_cells": validator.get_invalid_cells(validation_result["errors"])
    }