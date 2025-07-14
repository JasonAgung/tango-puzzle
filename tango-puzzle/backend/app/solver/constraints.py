"""
CSP constraint definitions for Tango puzzle
"""
from typing import List, Tuple, Optional, Dict
from enum import Enum
from ortools.sat.python import cp_model


class CellValue(Enum):
    EMPTY = 0
    SUN = 1
    MOON = 2


class ConstraintType(Enum):
    EQUAL = "equal"
    OPPOSITE = "opposite"


class TangoConstraints:
    """Defines all constraints for the Tango puzzle"""
    
    def __init__(self, size: int = 6):
        self.size = size
        self.model = cp_model.CpModel()
        self.cells = {}  # Dictionary to store cell variables
        self._create_variables()
    
    def _create_variables(self):
        """Create boolean variables for each cell and value combination"""
        for row in range(self.size):
            for col in range(self.size):
                # Create two boolean variables per cell (one for sun, one for moon)
                self.cells[(row, col, 'sun')] = self.model.NewBoolVar(f'cell_{row}_{col}_sun')
                self.cells[(row, col, 'moon')] = self.model.NewBoolVar(f'cell_{row}_{col}_moon')
    
    def add_basic_constraints(self):
        """Add basic puzzle constraints"""
        # Each cell must have exactly one value (sun or moon)
        for row in range(self.size):
            for col in range(self.size):
                sun_var = self.cells[(row, col, 'sun')]
                moon_var = self.cells[(row, col, 'moon')]
                # Exactly one must be true
                self.model.Add(sun_var + moon_var == 1)
    
    def add_row_constraints(self):
        """Each row must have exactly 3 suns and 3 moons"""
        for row in range(self.size):
            sun_vars = [self.cells[(row, col, 'sun')] for col in range(self.size)]
            moon_vars = [self.cells[(row, col, 'moon')] for col in range(self.size)]
            
            self.model.Add(sum(sun_vars) == 3)
            self.model.Add(sum(moon_vars) == 3)
    
    def add_column_constraints(self):
        """Each column must have exactly 3 suns and 3 moons"""
        for col in range(self.size):
            sun_vars = [self.cells[(row, col, 'sun')] for row in range(self.size)]
            moon_vars = [self.cells[(row, col, 'moon')] for row in range(self.size)]
            
            self.model.Add(sum(sun_vars) == 3)
            self.model.Add(sum(moon_vars) == 3)
    
    def add_consecutive_constraints(self):
        """No more than 2 of the same symbol may be consecutive (horizontally or vertically)"""
        # Horizontal consecutive constraints
        for row in range(self.size):
            for col in range(self.size - 2):
                # Check three consecutive cells
                sun_vars = [self.cells[(row, col + i, 'sun')] for i in range(3)]
                moon_vars = [self.cells[(row, col + i, 'moon')] for i in range(3)]
                
                # At most 2 suns in any 3 consecutive cells
                self.model.Add(sum(sun_vars) <= 2)
                # At most 2 moons in any 3 consecutive cells
                self.model.Add(sum(moon_vars) <= 2)
        
        # Vertical consecutive constraints
        for col in range(self.size):
            for row in range(self.size - 2):
                # Check three consecutive cells
                sun_vars = [self.cells[(row + i, col, 'sun')] for i in range(3)]
                moon_vars = [self.cells[(row + i, col, 'moon')] for i in range(3)]
                
                # At most 2 suns in any 3 consecutive cells
                self.model.Add(sum(sun_vars) <= 2)
                # At most 2 moons in any 3 consecutive cells
                self.model.Add(sum(moon_vars) <= 2)
    
    def add_equal_constraint(self, row1: int, col1: int, row2: int, col2: int):
        """Add constraint that two cells must have the same value"""
        # If cell1 is sun, cell2 must be sun
        self.model.Add(self.cells[(row1, col1, 'sun')] == self.cells[(row2, col2, 'sun')])
        # If cell1 is moon, cell2 must be moon
        self.model.Add(self.cells[(row1, col1, 'moon')] == self.cells[(row2, col2, 'moon')])
    
    def add_opposite_constraint(self, row1: int, col1: int, row2: int, col2: int):
        """Add constraint that two cells must have opposite values"""
        # If cell1 is sun, cell2 must be moon
        self.model.Add(self.cells[(row1, col1, 'sun')] == self.cells[(row2, col2, 'moon')])
        # If cell1 is moon, cell2 must be sun
        self.model.Add(self.cells[(row1, col1, 'moon')] == self.cells[(row2, col2, 'sun')])
    
    def add_given_value(self, row: int, col: int, value: str):
        """Fix a cell to a given value (for puzzle initialization)"""
        if value == 'sun':
            self.model.Add(self.cells[(row, col, 'sun')] == 1)
            self.model.Add(self.cells[(row, col, 'moon')] == 0)
        elif value == 'moon':
            self.model.Add(self.cells[(row, col, 'sun')] == 0)
            self.model.Add(self.cells[(row, col, 'moon')] == 1)
    
    def get_solution_grid(self, solver: cp_model.CpSolver) -> List[List[Optional[str]]]:
        """Extract the solution grid from the solver"""
        grid = []
        for row in range(self.size):
            row_values = []
            for col in range(self.size):
                if solver.Value(self.cells[(row, col, 'sun')]) == 1:
                    row_values.append('sun')
                elif solver.Value(self.cells[(row, col, 'moon')]) == 1:
                    row_values.append('moon')
                else:
                    row_values.append(None)
            grid.append(row_values)
        return grid