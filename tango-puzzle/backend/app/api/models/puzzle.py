from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


CellValue = Optional[Literal["sun", "moon"]]
ConstraintType = Literal["equal", "opposite"]
Difficulty = Literal["easy", "medium", "hard"]


class Constraint(BaseModel):
    type: ConstraintType
    row1: int = Field(..., ge=0, le=5)
    col1: int = Field(..., ge=0, le=5)
    row2: int = Field(..., ge=0, le=5)
    col2: int = Field(..., ge=0, le=5)


class PuzzleCreate(BaseModel):
    difficulty: Difficulty = "medium"


class PuzzleResponse(BaseModel):
    id: str
    grid: List[List[CellValue]]
    constraints: List[Constraint]
    difficulty: Difficulty
    created_at: Optional[datetime] = None


class PuzzleValidate(BaseModel):
    puzzle_id: str
    grid: List[List[CellValue]]


class GameState(BaseModel):
    puzzle_id: str
    grid: List[List[CellValue]]
    time_elapsed: int = 0
    moves_count: int = 0