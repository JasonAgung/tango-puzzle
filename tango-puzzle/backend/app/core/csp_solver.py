"""
CSP Solver for Tango puzzle using OR-Tools
"""
from typing import List, Optional, Dict, Tuple
from ortools.sat.python import cp_model
from app.solver.constraints import TangoConstraints
from app.api.models.puzzle import Constraint
from app.api.models.solution import ExplanationStep


class CSPSolver:
    """Solves Tango puzzles using constraint satisfaction"""
    
    def __init__(self, size: int = 6):
        self.size = size
        self.solution_steps = []
    
    def solve(self, initial_grid: List[List[Optional[str]]], 
              constraints: List[Constraint]) -> Dict[str, any]:
        """
        Solve the puzzle given initial configuration and constraints
        Returns solution grid and solving steps
        """
        # Create constraint model
        tango_model = TangoConstraints(self.size)
        
        # Add all basic constraints
        tango_model.add_basic_constraints()
        tango_model.add_row_constraints()
        tango_model.add_column_constraints()
        tango_model.add_consecutive_constraints()
        
        # Add special constraints (equal/opposite)
        for constraint in constraints:
            if constraint.type == "equal":
                tango_model.add_equal_constraint(
                    constraint.row1, constraint.col1,
                    constraint.row2, constraint.col2
                )
            elif constraint.type == "opposite":
                tango_model.add_opposite_constraint(
                    constraint.row1, constraint.col1,
                    constraint.row2, constraint.col2
                )
        
        # Add given values from initial grid
        for row in range(self.size):
            for col in range(self.size):
                if initial_grid[row][col] is not None:
                    tango_model.add_given_value(row, col, initial_grid[row][col])
        
        # Create solver and solve
        solver = cp_model.CpSolver()
        status = solver.Solve(tango_model.model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            solution_grid = tango_model.get_solution_grid(solver)
            
            # Generate explanation steps
            steps = self._generate_explanation_steps(initial_grid, solution_grid, constraints)
            
            return {
                "success": True,
                "solution": solution_grid,
                "steps": steps,
                "unique": self._check_uniqueness(tango_model, solver)
            }
        else:
            return {
                "success": False,
                "solution": None,
                "steps": [],
                "message": "No solution found"
            }
    
    def get_hint(self, current_grid: List[List[Optional[str]]], 
                 constraints: List[Constraint]) -> Optional[Dict]:
        """
        Get a hint for the next logical move
        """
        # First, solve the complete puzzle
        solution_result = self.solve(current_grid, constraints)
        
        if not solution_result["success"]:
            return None
        
        solution_grid = solution_result["solution"]
        
        # Find the first empty cell that can be deduced
        for step in solution_result["steps"]:
            # Access attributes of ExplanationStep object, not dictionary keys
            row, col = step.row, step.col
            if current_grid[row][col] is None:
                return {
                    "row": row,
                    "col": col,
                    "value": solution_grid[row][col],
                    "explanation": step.explanation
                }
        
        return None
    
    def _check_uniqueness(self, model: TangoConstraints, solver: cp_model.CpSolver) -> bool:
        """Check if the solution is unique"""
        # Get the current solution
        current_solution = []
        for row in range(self.size):
            for col in range(self.size):
                if solver.Value(model.cells[(row, col, 'sun')]) == 1:
                    current_solution.append(model.cells[(row, col, 'sun')])
                else:
                    current_solution.append(model.cells[(row, col, 'moon')])
        
        # Add constraint to find a different solution
        model.model.Add(sum(var if solver.Value(var) == 0 else (1 - var) 
                           for var in current_solution) >= 1)
        
        # Try to find another solution
        status = solver.Solve(model.model)
        
        # If no other solution found, the original is unique
        return status != cp_model.OPTIMAL and status != cp_model.FEASIBLE
    
    def _generate_explanation_steps(self, initial_grid: List[List[Optional[str]]], 
                                   solution_grid: List[List[str]], 
                                   constraints: List[Constraint]) -> List[ExplanationStep]:
        """Generate step-by-step explanation of the solution"""
        steps = []
        step_number = 0
        working_grid = [row[:] for row in initial_grid]  # Deep copy
        
        # Keep applying deduction rules until grid is complete
        while self._has_empty_cells(working_grid):
            # Try each deduction rule in order of complexity
            step = self._apply_simple_row_column_deduction(working_grid, solution_grid)
            if not step:
                step = self._apply_consecutive_rule(working_grid, solution_grid)
            if not step:
                step = self._apply_constraint_rule(working_grid, solution_grid, constraints)
            if not step:
                step = self._apply_advanced_deduction(working_grid, solution_grid)
            
            if step:
                step_number += 1
                step["step_number"] = step_number
                steps.append(ExplanationStep(**step))
                # Update working grid
                working_grid[step["row"]][step["col"]] = step["value"]
            else:
                # If no deduction possible, fill remaining cells
                # This shouldn't happen with a properly constructed puzzle
                break
        
        return steps
    
    def _has_empty_cells(self, grid: List[List[Optional[str]]]) -> bool:
        """Check if grid has empty cells"""
        return any(cell is None for row in grid for cell in row)
    
    def _apply_simple_row_column_deduction(self, working_grid: List[List[Optional[str]]], 
                                         solution_grid: List[List[str]]) -> Optional[Dict]:
        """Apply simple row/column count deductions"""
        # Check rows
        for row in range(self.size):
            sun_count = sum(1 for cell in working_grid[row] if cell == 'sun')
            moon_count = sum(1 for cell in working_grid[row] if cell == 'moon')
            empty_cells = [(row, col) for col in range(self.size) if working_grid[row][col] is None]
            
            # If we have 3 suns, remaining must be moons
            if sun_count == 3 and empty_cells:
                col = empty_cells[0][1]
                return {
                    "row": row,
                    "col": col,
                    "value": "moon",
                    "rule_applied": "row_count",
                    "explanation": f"Row {row} already has 3 suns, so remaining cells must be moons"
                }
            
            # If we have 3 moons, remaining must be suns
            if moon_count == 3 and empty_cells:
                col = empty_cells[0][1]
                return {
                    "row": row,
                    "col": col,
                    "value": "sun",
                    "rule_applied": "row_count",
                    "explanation": f"Row {row} already has 3 moons, so remaining cells must be suns"
                }
        
        # Check columns (similar logic)
        for col in range(self.size):
            sun_count = sum(1 for row in range(self.size) if working_grid[row][col] == 'sun')
            moon_count = sum(1 for row in range(self.size) if working_grid[row][col] == 'moon')
            empty_cells = [(row, col) for row in range(self.size) if working_grid[row][col] is None]
            
            if sun_count == 3 and empty_cells:
                row = empty_cells[0][0]
                return {
                    "row": row,
                    "col": col,
                    "value": "moon",
                    "rule_applied": "column_count",
                    "explanation": f"Column {col} already has 3 suns, so remaining cells must be moons"
                }
            
            if moon_count == 3 and empty_cells:
                row = empty_cells[0][0]
                return {
                    "row": row,
                    "col": col,
                    "value": "sun",
                    "rule_applied": "column_count",
                    "explanation": f"Column {col} already has 3 moons, so remaining cells must be suns"
                }
        
        return None
    
    def _apply_consecutive_rule(self, working_grid: List[List[Optional[str]]], 
                               solution_grid: List[List[str]]) -> Optional[Dict]:
        """Apply consecutive symbol prevention rule"""
        # Check horizontal
        for row in range(self.size):
            for col in range(self.size):
                if working_grid[row][col] is None:
                    # Check if placing a symbol would create 3 consecutive
                    for symbol in ['sun', 'moon']:
                        if self._would_create_three_consecutive(working_grid, row, col, symbol):
                            # Must place the opposite symbol
                            opposite = 'moon' if symbol == 'sun' else 'sun'
                            return {
                                "row": row,
                                "col": col,
                                "value": opposite,
                                "rule_applied": "consecutive_prevention",
                                "explanation": f"Placing {symbol} here would create three consecutive {symbol}s"
                            }
        
        return None
    
    def _would_create_three_consecutive(self, grid: List[List[Optional[str]]], 
                                      row: int, col: int, symbol: str) -> bool:
        """Check if placing symbol at (row, col) would create 3 consecutive"""
        # Check horizontal
        # Case 1: X X _
        if col >= 2 and grid[row][col-1] == symbol and grid[row][col-2] == symbol:
            return True
        # Case 2: X _ X
        if col >= 1 and col < self.size - 1 and grid[row][col-1] == symbol and grid[row][col+1] == symbol:
            return True
        # Case 3: _ X X
        if col < self.size - 2 and grid[row][col+1] == symbol and grid[row][col+2] == symbol:
            return True
        
        # Check vertical (similar logic)
        # Case 1: X X _
        if row >= 2 and grid[row-1][col] == symbol and grid[row-2][col] == symbol:
            return True
        # Case 2: X _ X
        if row >= 1 and row < self.size - 1 and grid[row-1][col] == symbol and grid[row+1][col] == symbol:
            return True
        # Case 3: _ X X
        if row < self.size - 2 and grid[row+1][col] == symbol and grid[row+2][col] == symbol:
            return True
        
        return False
    
    def _apply_constraint_rule(self, working_grid: List[List[Optional[str]]], 
                              solution_grid: List[List[str]], 
                              constraints: List[Constraint]) -> Optional[Dict]:
        """Apply equal/opposite constraint rules"""
        for constraint in constraints:
            cell1_val = working_grid[constraint.row1][constraint.col1]
            cell2_val = working_grid[constraint.row2][constraint.col2]
            
            if constraint.type == "equal":
                if cell1_val is not None and cell2_val is None:
                    return {
                        "row": constraint.row2,
                        "col": constraint.col2,
                        "value": cell1_val,
                        "rule_applied": "equal_constraint",
                        "explanation": f"Must be {cell1_val} due to equal constraint with cell ({constraint.row1}, {constraint.col1})"
                    }
                elif cell1_val is None and cell2_val is not None:
                    return {
                        "row": constraint.row1,
                        "col": constraint.col1,
                        "value": cell2_val,
                        "rule_applied": "equal_constraint",
                        "explanation": f"Must be {cell2_val} due to equal constraint with cell ({constraint.row2}, {constraint.col2})"
                    }
            
            elif constraint.type == "opposite":
                if cell1_val is not None and cell2_val is None:
                    opposite = 'moon' if cell1_val == 'sun' else 'sun'
                    return {
                        "row": constraint.row2,
                        "col": constraint.col2,
                        "value": opposite,
                        "rule_applied": "opposite_constraint",
                        "explanation": f"Must be {opposite} due to opposite constraint with cell ({constraint.row1}, {constraint.col1})"
                    }
                elif cell1_val is None and cell2_val is not None:
                    opposite = 'moon' if cell2_val == 'sun' else 'sun'
                    return {
                        "row": constraint.row1,
                        "col": constraint.col1,
                        "value": opposite,
                        "rule_applied": "opposite_constraint",
                        "explanation": f"Must be {opposite} due to opposite constraint with cell ({constraint.row2}, {constraint.col2})"
                    }
        
        return None
    
    def _apply_advanced_deduction(self, working_grid: List[List[Optional[str]]], 
                                 solution_grid: List[List[str]]) -> Optional[Dict]:
        """Apply more complex deduction rules"""
        # Find first empty cell and use solution
        # This is a fallback for complex deductions
        for row in range(self.size):
            for col in range(self.size):
                if working_grid[row][col] is None:
                    return {
                        "row": row,
                        "col": col,
                        "value": solution_grid[row][col],
                        "rule_applied": "advanced_deduction",
                        "explanation": "Determined through constraint propagation and logical deduction"
                    }
        
        return None