"""
Constraint validator for Tango puzzle
Validates game rules without solving the entire puzzle
"""
from typing import List, Optional, Tuple, Dict
from app.api.models.puzzle import Constraint


class ConstraintValidator:
    """Validates Tango puzzle constraints"""
    
    def __init__(self, size: int = 6):
        self.size = size
    
    def validate_grid(self, grid: List[List[Optional[str]]], constraints: List[Constraint]) -> Dict[str, any]:
        """
        Validate the current state of the grid
        Returns a dictionary with validation results
        """
        errors = []
        is_complete = True
        
        # Check if grid is complete (no empty cells)
        for row in range(self.size):
            for col in range(self.size):
                if grid[row][col] is None:
                    is_complete = False
        
        # Validate row constraints
        row_errors = self._validate_rows(grid)
        errors.extend(row_errors)
        
        # Validate column constraints
        col_errors = self._validate_columns(grid)
        errors.extend(col_errors)
        
        # Validate consecutive constraints
        consecutive_errors = self._validate_consecutive(grid)
        errors.extend(consecutive_errors)
        
        # Validate special constraints (equal/opposite)
        constraint_errors = self._validate_special_constraints(grid, constraints)
        errors.extend(constraint_errors)
        
        return {
            "valid": len(errors) == 0,
            "complete": is_complete and len(errors) == 0,
            "errors": errors
        }
    
    def _validate_rows(self, grid: List[List[Optional[str]]]) -> List[Dict]:
        """Validate that each row has at most 3 suns and 3 moons"""
        errors = []
        
        for row in range(self.size):
            sun_count = sum(1 for cell in grid[row] if cell == 'sun')
            moon_count = sum(1 for cell in grid[row] if cell == 'moon')
            
            if sun_count > 3:
                errors.append({
                    "type": "row_count",
                    "row": row,
                    "message": f"Row {row} has {sun_count} suns (max 3)"
                })
            
            if moon_count > 3:
                errors.append({
                    "type": "row_count",
                    "row": row,
                    "message": f"Row {row} has {moon_count} moons (max 3)"
                })
            
            # If row is complete, check exact counts
            if sun_count + moon_count == self.size:
                if sun_count != 3 or moon_count != 3:
                    errors.append({
                        "type": "row_balance",
                        "row": row,
                        "message": f"Row {row} must have exactly 3 suns and 3 moons"
                    })
        
        return errors
    
    def _validate_columns(self, grid: List[List[Optional[str]]]) -> List[Dict]:
        """Validate that each column has at most 3 suns and 3 moons"""
        errors = []
        
        for col in range(self.size):
            sun_count = sum(1 for row in range(self.size) if grid[row][col] == 'sun')
            moon_count = sum(1 for row in range(self.size) if grid[row][col] == 'moon')
            
            if sun_count > 3:
                errors.append({
                    "type": "column_count",
                    "col": col,
                    "message": f"Column {col} has {sun_count} suns (max 3)"
                })
            
            if moon_count > 3:
                errors.append({
                    "type": "column_count",
                    "col": col,
                    "message": f"Column {col} has {moon_count} moons (max 3)"
                })
            
            # If column is complete, check exact counts
            if sun_count + moon_count == self.size:
                if sun_count != 3 or moon_count != 3:
                    errors.append({
                        "type": "column_balance",
                        "col": col,
                        "message": f"Column {col} must have exactly 3 suns and 3 moons"
                    })
        
        return errors
    
    def _validate_consecutive(self, grid: List[List[Optional[str]]]) -> List[Dict]:
        """Validate no more than 2 consecutive same symbols"""
        errors = []
        
        # Check horizontal consecutive
        for row in range(self.size):
            for col in range(self.size - 2):
                cells = [grid[row][col + i] for i in range(3)]
                # Skip if any cell is empty
                if None in cells:
                    continue
                
                if cells[0] == cells[1] == cells[2]:
                    errors.append({
                        "type": "consecutive_horizontal",
                        "cells": [(row, col + i) for i in range(3)],
                        "message": f"Three consecutive {cells[0]}s in row {row}"
                    })
        
        # Check vertical consecutive
        for col in range(self.size):
            for row in range(self.size - 2):
                cells = [grid[row + i][col] for i in range(3)]
                # Skip if any cell is empty
                if None in cells:
                    continue
                
                if cells[0] == cells[1] == cells[2]:
                    errors.append({
                        "type": "consecutive_vertical",
                        "cells": [(row + i, col) for i in range(3)],
                        "message": f"Three consecutive {cells[0]}s in column {col}"
                    })
        
        return errors
    
    def _validate_special_constraints(self, grid: List[List[Optional[str]]], 
                                    constraints: List[Constraint]) -> List[Dict]:
        """Validate equal and opposite constraints"""
        errors = []
        
        for constraint in constraints:
            cell1 = grid[constraint.row1][constraint.col1]
            cell2 = grid[constraint.row2][constraint.col2]
            
            # Skip if either cell is empty
            if cell1 is None or cell2 is None:
                continue
            
            if constraint.type == "equal":
                if cell1 != cell2:
                    errors.append({
                        "type": "equal_constraint",
                        "cells": [(constraint.row1, constraint.col1), 
                                (constraint.row2, constraint.col2)],
                        "message": f"Cells must have the same value"
                    })
            
            elif constraint.type == "opposite":
                if cell1 == cell2:
                    errors.append({
                        "type": "opposite_constraint",
                        "cells": [(constraint.row1, constraint.col1), 
                                (constraint.row2, constraint.col2)],
                        "message": f"Cells must have opposite values"
                    })
        
        return errors
    
    def get_invalid_cells(self, errors: List[Dict]) -> List[Tuple[int, int]]:
        """Extract list of invalid cell positions from errors"""
        invalid_cells = set()
        
        for error in errors:
            if 'cells' in error:
                for cell in error['cells']:
                    invalid_cells.add(cell)
            elif 'row' in error:
                # Add all cells in the row
                row = error['row']
                for col in range(self.size):
                    invalid_cells.add((row, col))
            elif 'col' in error:
                # Add all cells in the column
                col = error['col']
                for row in range(self.size):
                    invalid_cells.add((row, col))
        
        return list(invalid_cells)