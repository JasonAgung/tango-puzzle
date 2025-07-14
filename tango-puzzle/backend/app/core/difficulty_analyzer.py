"""
Difficulty analyzer for Tango puzzles
Analyzes puzzle difficulty based on required deduction techniques
"""
from typing import List, Dict, Optional
from app.core.csp_solver import CSPSolver
from app.api.models.puzzle import Constraint, Difficulty


class DifficultyAnalyzer:
    """Analyzes and rates puzzle difficulty"""
    
    def __init__(self, size: int = 6):
        self.size = size
        self.solver = CSPSolver(size)
    
    def analyze_difficulty(self, puzzle_grid: List[List[Optional[str]]], 
                         constraints: List[Constraint]) -> Dict:
        """
        Analyze puzzle difficulty based on solving steps
        Returns difficulty metrics
        """
        # Solve the puzzle and get steps
        solver_result = self.solver.solve(puzzle_grid, constraints)
        
        if not solver_result["success"]:
            return {
                "difficulty": None,
                "solvable": False,
                "metrics": {}
            }
        
        steps = solver_result["steps"]
        
        # Count different types of deductions used
        deduction_counts = {
            "row_count": 0,
            "column_count": 0,
            "consecutive_prevention": 0,
            "equal_constraint": 0,
            "opposite_constraint": 0,
            "advanced_deduction": 0
        }
        
        for step in steps:
            rule = step.rule_applied
            if rule in deduction_counts:
                deduction_counts[rule] += 1
        
        # Calculate difficulty score
        difficulty_score = self._calculate_difficulty_score(deduction_counts, len(steps))
        
        # Determine difficulty level
        if difficulty_score <= 30:
            difficulty_level = "easy"
        elif difficulty_score <= 60:
            difficulty_level = "medium"
        else:
            difficulty_level = "hard"
        
        return {
            "difficulty": difficulty_level,
            "solvable": True,
            "unique": solver_result["unique"],
            "metrics": {
                "total_steps": len(steps),
                "deduction_counts": deduction_counts,
                "difficulty_score": difficulty_score,
                "given_cells": sum(1 for row in puzzle_grid for cell in row if cell is not None),
                "constraint_count": len(constraints)
            }
        }
    
    def _calculate_difficulty_score(self, deduction_counts: Dict[str, int], 
                                  total_steps: int) -> float:
        """
        Calculate a difficulty score based on deduction types used
        Higher score = harder puzzle
        """
        # Weight different deduction types
        weights = {
            "row_count": 1.0,              # Simple
            "column_count": 1.0,           # Simple
            "consecutive_prevention": 2.0,  # Medium
            "equal_constraint": 1.5,       # Medium
            "opposite_constraint": 1.5,    # Medium
            "advanced_deduction": 3.0      # Hard
        }
        
        # Calculate weighted sum
        weighted_sum = sum(count * weights.get(rule, 1.0) 
                          for rule, count in deduction_counts.items())
        
        # Factor in total steps (more steps = harder)
        step_factor = min(total_steps / 20, 2.0)  # Cap at 2x
        
        # Calculate final score (0-100 scale)
        score = (weighted_sum * step_factor * 10) / max(total_steps, 1)
        
        return min(score, 100)  # Cap at 100
    
    def suggest_difficulty_adjustments(self, current_difficulty: Dict) -> Dict:
        """
        Suggest how to adjust puzzle to match target difficulty
        """
        suggestions = []
        metrics = current_difficulty.get("metrics", {})
        
        if current_difficulty["difficulty"] == "easy":
            if metrics.get("given_cells", 0) < 20:
                suggestions.append("Add more given cells to make it easier")
            if metrics.get("constraint_count", 0) < 3:
                suggestions.append("Add more constraints to provide more clues")
        
        elif current_difficulty["difficulty"] == "hard":
            if metrics.get("given_cells", 0) > 14:
                suggestions.append("Remove some given cells to make it harder")
            if metrics.get("deduction_counts", {}).get("advanced_deduction", 0) < 2:
                suggestions.append("Adjust puzzle to require more complex deductions")
        
        return {
            "current_difficulty": current_difficulty["difficulty"],
            "suggestions": suggestions,
            "metrics": metrics
        }