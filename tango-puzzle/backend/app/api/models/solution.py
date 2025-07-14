from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from app.api.models.puzzle import CellValue


class SolveRequest(BaseModel):
    puzzle_id: str
    current_grid: List[List[CellValue]]


class ExplanationStep(BaseModel):
    step_number: int
    row: int = Field(..., ge=0, le=5)
    col: int = Field(..., ge=0, le=5)
    value: Literal["sun", "moon"]
    rule_applied: str
    explanation: str


class SolutionResponse(BaseModel):
    puzzle_id: str
    solution: List[List[CellValue]]
    steps: List[ExplanationStep]


class HintResponse(BaseModel):
    row: int = Field(..., ge=0, le=5)
    col: int = Field(..., ge=0, le=5)
    value: Literal["sun", "moon"]
    explanation: str