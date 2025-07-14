"""
Puzzle generator for Tango puzzle
Generates puzzles with unique solutions and controlled difficulty
"""
import random
from typing import List, Optional, Tuple, Dict
from app.solver.constraints import TangoConstraints
from app.core.csp_solver import CSPSolver
from app.core.constraint_validator import ConstraintValidator
from app.api.models.puzzle import Constraint, Difficulty
from ortools.sat.python import cp_model


class PuzzleGenerator:
    """Generates Tango puzzles with varying difficulty"""
    
    def __init__(self, size: int = 6):
        self.size = size
        self.solver = CSPSolver(size)
        self.validator = ConstraintValidator(size)
    
    def generate_puzzle(self, difficulty: Difficulty = "medium") -> Dict:
        """
        Generate a new puzzle with specified difficulty
        Returns puzzle configuration with unique solution
        """
        # First, generate a complete valid solution
        solution_grid = self._generate_complete_solution()
        
        # Generate constraints based on difficulty
        constraints = self._generate_constraints(solution_grid, difficulty)
        
        # Create puzzle by removing values while maintaining unique solution
        puzzle_grid = self._create_puzzle_from_solution(solution_grid, constraints, difficulty)
        
        # Verify the puzzle has a unique solution
        solver_result = self.solver.solve(puzzle_grid, constraints)
        
        if not solver_result["success"] or not solver_result["unique"]:
            # If puzzle is not valid, try again
            return self.generate_puzzle(difficulty)
        
        return {
            "grid": puzzle_grid,
            "constraints": constraints,
            "solution": solution_grid,
            "difficulty": difficulty,
            "given_count": sum(1 for row in puzzle_grid for cell in row if cell is not None)
        }
    
    def _generate_complete_solution(self) -> List[List[str]]:
        """Generate a random complete valid grid"""
        # Use CSP to generate a random valid solution
        model = TangoConstraints(self.size)
        model.add_basic_constraints()
        model.add_row_constraints()
        model.add_column_constraints()
        model.add_consecutive_constraints()
        
        # Add randomization by randomly fixing some cells
        # This helps generate different solutions
        random_cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(random_cells)
        
        # Try to fix a few random cells to guide the solution
        for i in range(min(3, len(random_cells))):
            row, col = random_cells[i]
            value = random.choice(['sun', 'moon'])
            model.add_given_value(row, col, value)
        
        # Solve with randomization
        solver = cp_model.CpSolver()
        solver.parameters.random_seed = random.randint(0, 10000)
        solver.parameters.num_search_workers = 1
        
        status = solver.Solve(model.model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            return model.get_solution_grid(solver)
        else:
            # If failed, try again with different random seed
            return self._generate_complete_solution()
    
    def _generate_constraints(self, solution_grid: List[List[str]], 
                            difficulty: Difficulty) -> List[Constraint]:
        """Generate equal/opposite constraints based on difficulty"""
        constraints = []
        
        # Number of constraints based on difficulty
        constraint_counts = {
            "easy": (4, 6),     # 4-6 constraints
            "medium": (6, 10),   # 6-10 constraints
            "hard": (10, 15)     # 10-15 constraints
        }
        
        min_constraints, max_constraints = constraint_counts.get(difficulty, (5, 8))
        num_constraints = random.randint(min_constraints, max_constraints)
        
        # Generate adjacent cell pairs
        adjacent_pairs = []
        
        # Horizontal pairs (only between adjacent cells within grid)
        for row in range(self.size):
            for col in range(self.size - 1):  # Stop before last column
                adjacent_pairs.append(((row, col), (row, col + 1)))
        
        # Vertical pairs (only between adjacent cells within grid)
        for row in range(self.size - 1):  # Stop before last row
            for col in range(self.size):
                adjacent_pairs.append(((row, col), (row + 1, col)))
        
        # Randomly select pairs for constraints
        random.shuffle(adjacent_pairs)
        
        for i in range(min(num_constraints, len(adjacent_pairs))):
            (row1, col1), (row2, col2) = adjacent_pairs[i]
            
            # Validate that cells are actually adjacent
            if not (
                (row1 == row2 and abs(col1 - col2) == 1) or 
                (col1 == col2 and abs(row1 - row2) == 1)
            ):
                continue  # Skip invalid pairs
            
            # Determine constraint type based on actual values
            if solution_grid[row1][col1] == solution_grid[row2][col2]:
                constraint_type = "equal"
            else:
                constraint_type = "opposite"
            
            constraints.append(Constraint(
                type=constraint_type,
                row1=row1,
                col1=col1,
                row2=row2,
                col2=col2
            ))
        
        return constraints
    
    def _create_puzzle_from_solution(self, solution_grid: List[List[str]], 
                                   constraints: List[Constraint],
                                   difficulty: Difficulty) -> List[List[Optional[str]]]:
        """Create puzzle by removing values while maintaining uniqueness"""
        # Start with complete solution
        puzzle_grid = [[solution_grid[r][c] for c in range(self.size)] 
                      for r in range(self.size)]
        
        # Number of given cells based on difficulty
        given_counts = {
            "easy": (22, 26),    # 22-26 given cells (more clues)
            "medium": (12, 16),   # 12-16 given cells
            "hard": (6, 10)      # 6-10 given cells (much fewer clues)
        }
        
        min_given, max_given = given_counts.get(difficulty, (14, 18))
        target_given = random.randint(min_given, max_given)
        
        # For hard difficulty, prioritize removing cells that make the puzzle harder
        if difficulty == "hard":
            return self._create_hard_puzzle(solution_grid, constraints, target_given)
        
        # Create list of all cells
        all_cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(all_cells)
        
        # Remove cells one by one while maintaining unique solution
        cells_removed = 0
        current_given = self.size * self.size
        
        for row, col in all_cells:
            if current_given <= target_given:
                break
            
            # Try removing this cell
            temp_value = puzzle_grid[row][col]
            puzzle_grid[row][col] = None
            
            # Check if puzzle still has unique solution
            solver_result = self.solver.solve(puzzle_grid, constraints)
            
            if solver_result["success"] and solver_result["unique"]:
                # Successfully removed
                cells_removed += 1
                current_given -= 1
            else:
                # Put it back
                puzzle_grid[row][col] = temp_value
        
        # Ensure we have some symmetry for aesthetics
        puzzle_grid = self._apply_symmetry(puzzle_grid, solution_grid)
        
        return puzzle_grid
    
    def _apply_symmetry(self, puzzle_grid: List[List[Optional[str]]], 
                       solution_grid: List[List[str]]) -> List[List[Optional[str]]]:
        """Apply rotational symmetry to the puzzle for aesthetics"""
        # For each given cell, try to add its rotationally symmetric counterpart
        symmetric_grid = [[puzzle_grid[r][c] for c in range(self.size)] 
                         for r in range(self.size)]
        
        for row in range(self.size):
            for col in range(self.size):
                if puzzle_grid[row][col] is not None:
                    # Calculate symmetric position (180 degree rotation)
                    sym_row = self.size - 1 - row
                    sym_col = self.size - 1 - col
                    
                    # If symmetric position is empty and adding it maintains uniqueness
                    if symmetric_grid[sym_row][sym_col] is None:
                        symmetric_grid[sym_row][sym_col] = solution_grid[sym_row][sym_col]
        
        # Verify the symmetric puzzle still has unique solution
        solver_result = self.solver.solve(symmetric_grid, [])
        
        if solver_result["success"] and solver_result["unique"]:
            return symmetric_grid
        else:
            # If symmetry breaks uniqueness, return original
            return puzzle_grid
    
    def _create_hard_puzzle(self, solution_grid: List[List[str]], 
                           constraints: List[Constraint],
                           target_given: int) -> List[List[Optional[str]]]:
        """Create a hard puzzle by strategic cell removal"""
        puzzle_grid = [[solution_grid[r][c] for c in range(self.size)] 
                      for r in range(self.size)]
        
        # Priority removal order for hard puzzles
        # 1. Remove cells that are not directly constrained
        # 2. Remove cells in the middle of rows/columns
        # 3. Keep minimal cells that force complex deductions
        
        removal_priority = []
        
        # Find cells involved in constraints
        constrained_cells = set()
        for constraint in constraints:
            constrained_cells.add((constraint.row1, constraint.col1))
            constrained_cells.add((constraint.row2, constraint.col2))
        
        # Prioritize unconstrained cells for removal
        for r in range(self.size):
            for c in range(self.size):
                if (r, c) not in constrained_cells:
                    removal_priority.append((r, c))
        
        # Add constrained cells last (remove these to make it harder)
        for cell in constrained_cells:
            removal_priority.append(cell)
        
        # Try to remove cells
        current_given = self.size * self.size
        for row, col in removal_priority:
            if current_given <= target_given:
                break
            
            # Try removing this cell
            temp_value = puzzle_grid[row][col]
            puzzle_grid[row][col] = None
            
            # Check if puzzle still has unique solution
            solver_result = self.solver.solve(puzzle_grid, constraints)
            
            if solver_result["success"] and solver_result["unique"]:
                current_given -= 1
            else:
                # Put it back
                puzzle_grid[row][col] = temp_value
        
        return puzzle_grid
    
    def validate_puzzle(self, puzzle_grid: List[List[Optional[str]]], 
                       constraints: List[Constraint]) -> bool:
        """Validate that a puzzle has exactly one solution"""
        solver_result = self.solver.solve(puzzle_grid, constraints)
        return solver_result["success"] and solver_result["unique"]