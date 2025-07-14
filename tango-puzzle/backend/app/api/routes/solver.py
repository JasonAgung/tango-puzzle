from fastapi import APIRouter, HTTPException
from typing import Dict, List, Optional
from app.api.models.solution import SolveRequest, SolutionResponse, HintResponse, ExplanationStep
from app.core.csp_solver import CSPSolver
from app.core.explanation_engine import ExplanationEngine
from app.api.routes.puzzle import puzzle_storage

router = APIRouter()


@router.post("/solve", response_model=SolutionResponse)
async def solve_puzzle(solve_request: SolveRequest):
    """Get complete solution for a puzzle"""
    solver = CSPSolver()
    
    # Get puzzle constraints
    if solve_request.puzzle_id not in puzzle_storage:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    constraints = puzzle_storage[solve_request.puzzle_id]["puzzle_data"]["constraints"]
    
    # Solve the puzzle
    result = solver.solve(solve_request.current_grid, constraints)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail="Puzzle cannot be solved from current state")
    
    return SolutionResponse(
        puzzle_id=solve_request.puzzle_id,
        solution=result["solution"],
        steps=result["steps"]
    )


@router.post("/hint", response_model=HintResponse)
async def get_hint(solve_request: SolveRequest):
    """Get next logical move as a hint"""
    solver = CSPSolver()
    
    # Get puzzle constraints
    if solve_request.puzzle_id not in puzzle_storage:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    constraints = puzzle_storage[solve_request.puzzle_id]["puzzle_data"]["constraints"]
    
    # Get hint
    hint = solver.get_hint(solve_request.current_grid, constraints)
    
    if not hint:
        raise HTTPException(status_code=400, detail="No hint available - puzzle may be complete or unsolvable")
    
    return HintResponse(
        row=hint["row"],
        col=hint["col"],
        value=hint["value"],
        explanation=hint["explanation"]
    )


@router.post("/explain")
async def get_explanation(solve_request: SolveRequest):
    """Get step-by-step explanation of the solution"""
    solver = CSPSolver()
    explanation_engine = ExplanationEngine()
    
    # Get puzzle constraints
    if solve_request.puzzle_id not in puzzle_storage:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    constraints = puzzle_storage[solve_request.puzzle_id]["puzzle_data"]["constraints"]
    
    # Solve and get steps
    result = solver.solve(solve_request.current_grid, constraints)
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail="Puzzle cannot be solved from current state")
    
    # Generate detailed explanations for each step
    detailed_steps = []
    for step in result["steps"]:
        detailed_step = explanation_engine.generate_step_explanation(step.__dict__)
        detailed_steps.append(detailed_step)
    
    # Generate solution summary
    summary = explanation_engine.generate_solution_summary(result["steps"])
    
    return {
        "steps": detailed_steps,
        "summary": summary
    }


@router.post("/check", response_model=Dict[str, bool])
async def check_solvability(solve_request: SolveRequest):
    """Check if current state is solvable"""
    solver = CSPSolver()
    
    # Get puzzle constraints
    if solve_request.puzzle_id not in puzzle_storage:
        raise HTTPException(status_code=404, detail="Puzzle not found")
    
    constraints = puzzle_storage[solve_request.puzzle_id]["puzzle_data"]["constraints"]
    
    # Check solvability
    result = solver.solve(solve_request.current_grid, constraints)
    
    return {
        "solvable": result["success"],
        "unique": result.get("unique", False)
    }