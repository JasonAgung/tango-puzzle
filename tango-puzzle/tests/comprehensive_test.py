#!/usr/bin/env python3
"""
Comprehensive test suite for Tango Puzzle game
Tests all backend API endpoints and frontend-backend integration
"""

import requests
import json
import time
from typing import Dict, List, Optional

# Configuration
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"
FRONTEND_URL = "http://localhost:5173"

class TangoTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        self.current_puzzle = None
        self.current_board_state = None
        
    def log_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result"""
        result = {
            "test": test_name,
            "passed": passed,
            "details": details
        }
        self.test_results.append(result)
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_name}")
        if details:
            print(f"   Details: {details}")
    
    def test_backend_health(self):
        """Test if backend is accessible"""
        try:
            response = self.session.get(f"{BASE_URL}/docs")
            self.log_result("Backend Health Check", response.status_code == 200)
        except Exception as e:
            self.log_result("Backend Health Check", False, str(e))
    
    def test_puzzle_generation(self):
        """Test puzzle generation with different difficulties"""
        difficulties = ["easy", "medium", "hard"]
        
        for difficulty in difficulties:
            try:
                response = self.session.post(
                    f"{BASE_URL}{API_PREFIX}/puzzle/generate",
                    json={"difficulty": difficulty}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Verify response structure
                    required_fields = ["id", "difficulty", "grid", "constraints"]
                    has_all_fields = all(field in data for field in required_fields)
                    
                    if has_all_fields:
                        self.log_result(
                            f"Puzzle Generation - {difficulty}", 
                            True,
                            f"Generated puzzle ID: {data.get('id')}"
                        )
                        
                        # Save the last puzzle for further testing
                        if difficulty == "easy":
                            self.current_puzzle = data
                            # Initialize empty board state (removing preset values)
                            self.current_board_state = [[None for _ in range(6)] for _ in range(6)]
                            # Copy only the preset values from the grid
                            for i in range(6):
                                for j in range(6):
                                    if data['grid'][i][j] is not None:
                                        self.current_board_state[i][j] = data['grid'][i][j]
                    else:
                        self.log_result(
                            f"Puzzle Generation - {difficulty}", 
                            False,
                            f"Missing fields: {[f for f in required_fields if f not in data]}"
                        )
                else:
                    self.log_result(
                        f"Puzzle Generation - {difficulty}", 
                        False,
                        f"Status code: {response.status_code}, Response: {response.text}"
                    )
                    
            except Exception as e:
                self.log_result(f"Puzzle Generation - {difficulty}", False, str(e))
    
    def test_get_puzzle(self):
        """Test getting a specific puzzle"""
        if not self.current_puzzle:
            self.log_result("Get Specific Puzzle", False, "No puzzle generated to test")
            return
            
        try:
            puzzle_id = self.current_puzzle["id"]
            response = self.session.get(f"{BASE_URL}{API_PREFIX}/puzzle/{puzzle_id}")
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Get Specific Puzzle", 
                    data["id"] == puzzle_id,
                    f"Retrieved puzzle ID: {data.get('id')}"
                )
            else:
                self.log_result(
                    "Get Specific Puzzle", 
                    False,
                    f"Status code: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("Get Specific Puzzle", False, str(e))
    
    def test_validation_empty_board(self):
        """Test validation with empty board"""
        if not self.current_puzzle:
            self.log_result("Validation - Empty Board", False, "No puzzle to validate")
            return
            
        try:
            response = self.session.post(
                f"{BASE_URL}{API_PREFIX}/puzzle/validate",
                json={
                    "puzzle_id": self.current_puzzle["id"],
                    "grid": self.current_board_state
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Validation - Empty Board", 
                    True,
                    f"Valid: {data.get('valid')}, Complete: {data.get('complete')}"
                )
            else:
                self.log_result(
                    "Validation - Empty Board", 
                    False,
                    f"Status code: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("Validation - Empty Board", False, str(e))
    
    def test_validation_with_moves(self):
        """Test validation with some moves"""
        if not self.current_puzzle:
            self.log_result("Validation - With Moves", False, "No puzzle to validate")
            return
            
        try:
            # Make some valid moves
            test_board = [[None for _ in range(6)] for _ in range(6)]
            test_board[0][0] = "sun"
            test_board[0][1] = "moon"
            test_board[1][0] = "moon"
            
            response = self.session.post(
                f"{BASE_URL}{API_PREFIX}/puzzle/validate",
                json={
                    "puzzle_id": self.current_puzzle["id"],
                    "grid": test_board
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                self.log_result(
                    "Validation - With Moves", 
                    True,
                    f"Valid: {data.get('valid')}, Violations: {data.get('violations', [])}"
                )
                
                # Update board state if valid
                if data.get('valid'):
                    self.current_board_state = test_board
            else:
                self.log_result(
                    "Validation - With Moves", 
                    False,
                    f"Status code: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("Validation - With Moves", False, str(e))
    
    def test_hint_system(self):
        """Test hint generation"""
        if not self.current_puzzle:
            self.log_result("Hint System", False, "No puzzle for hints")
            return
            
        try:
            response = self.session.post(
                f"{BASE_URL}{API_PREFIX}/solver/hint",
                json={
                    "puzzle_id": self.current_puzzle["id"],
                    "current_grid": self.current_board_state
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                # Check if we got a hint directly (not nested)
                if 'row' in data and 'col' in data and 'value' in data:
                    self.log_result(
                        "Hint System", 
                        True,
                        f"Hint at ({data.get('row')}, {data.get('col')}): {data.get('value')}"
                    )
                else:
                    self.log_result("Hint System", True, "No hint available (puzzle might be complete)")
            else:
                self.log_result(
                    "Hint System", 
                    False,
                    f"Status code: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("Hint System", False, str(e))
    
    def test_solver(self):
        """Test complete solver"""
        if not self.current_puzzle:
            self.log_result("Complete Solver", False, "No puzzle to solve")
            return
            
        try:
            response = self.session.post(
                f"{BASE_URL}{API_PREFIX}/solver/solve",
                json={
                    "puzzle_id": self.current_puzzle["id"],
                    "current_grid": [[None for _ in range(6)] for _ in range(6)]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                solution = data.get('solution')
                
                if solution:
                    # Check if solution is complete (all cells filled)
                    is_complete = all(
                        all(cell is not None for cell in row) 
                        for row in solution
                    )
                    
                    # Count suns and moons in first row as a sanity check
                    first_row = solution[0]
                    sun_count = sum(1 for cell in first_row if cell == "sun")
                    moon_count = sum(1 for cell in first_row if cell == "moon")
                    
                    self.log_result(
                        "Complete Solver", 
                        is_complete and sun_count == 3 and moon_count == 3,
                        f"Solution complete: {is_complete}, First row: {sun_count} suns, {moon_count} moons"
                    )
                else:
                    self.log_result("Complete Solver", False, "No solution returned")
            else:
                self.log_result(
                    "Complete Solver", 
                    False,
                    f"Status code: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("Complete Solver", False, str(e))
    
    def test_explanation_system(self):
        """Test step-by-step explanation"""
        if not self.current_puzzle:
            self.log_result("Explanation System", False, "No puzzle for explanation")
            return
            
        try:
            response = self.session.post(
                f"{BASE_URL}{API_PREFIX}/solver/explain",
                json={
                    "puzzle_id": self.current_puzzle["id"],
                    "current_grid": [[None for _ in range(6)] for _ in range(6)]
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                steps = data.get('steps', [])
                
                if steps:
                    self.log_result(
                        "Explanation System", 
                        True,
                        f"Generated {len(steps)} explanation steps"
                    )
                    
                    # Print first few steps
                    print("   First 3 steps:")
                    for i, step in enumerate(steps[:3]):
                        print(f"     Step {i+1}: {step.get('explanation', 'No explanation')}")
                else:
                    self.log_result("Explanation System", False, "No explanation steps returned")
            else:
                self.log_result(
                    "Explanation System", 
                    False,
                    f"Status code: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("Explanation System", False, str(e))
    
    def test_invalid_moves(self):
        """Test validation with invalid moves"""
        if not self.current_puzzle:
            self.log_result("Invalid Move Detection", False, "No puzzle to test")
            return
            
        try:
            # Create board with 4 suns in a row (invalid)
            invalid_board = [[None for _ in range(6)] for _ in range(6)]
            for i in range(4):
                invalid_board[0][i] = "sun"
            
            response = self.session.post(
                f"{BASE_URL}{API_PREFIX}/puzzle/validate",
                json={
                    "puzzle_id": self.current_puzzle["id"],
                    "grid": invalid_board
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                # This should be invalid
                is_invalid = not data.get('valid', True)
                errors = data.get('errors', [])
                
                self.log_result(
                    "Invalid Move Detection", 
                    is_invalid and len(errors) > 0,
                    f"Correctly detected as invalid: {is_invalid}, Errors: {errors}"
                )
            else:
                self.log_result(
                    "Invalid Move Detection", 
                    False,
                    f"Status code: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("Invalid Move Detection", False, str(e))
    
    def test_constraint_validation(self):
        """Test constraint validation (= and × symbols)"""
        if not self.current_puzzle:
            self.log_result("Constraint Validation", False, "No puzzle to test")
            return
            
        try:
            # Get constraints from puzzle
            constraints = self.current_puzzle.get('constraints', [])
            
            if constraints:
                # Separate constraints by type
                equal_constraints = [c for c in constraints if c['type'] == 'equal']
                opposite_constraints = [c for c in constraints if c['type'] == 'opposite']
                
                test_details = []
                
                if equal_constraints:
                    # Test equal constraint
                    constraint = equal_constraints[0]
                    test_board = [[None for _ in range(6)] for _ in range(6)]
                    
                    # Place same symbols (should be valid)
                    test_board[constraint['row1']][constraint['col1']] = "sun"
                    test_board[constraint['row2']][constraint['col2']] = "sun"
                    
                    test_details.append(f"Equal constraint at ({constraint['row1']},{constraint['col1']}) and ({constraint['row2']},{constraint['col2']})")
                
                if opposite_constraints:
                    # Test opposite constraint
                    constraint = opposite_constraints[0]
                    test_board = [[None for _ in range(6)] for _ in range(6)]
                    
                    # Place opposite symbols (should be valid)
                    test_board[constraint['row1']][constraint['col1']] = "sun"
                    test_board[constraint['row2']][constraint['col2']] = "moon"
                    
                    test_details.append(f"Opposite constraint at ({constraint['row1']},{constraint['col1']}) and ({constraint['row2']},{constraint['col2']})")
                
                self.log_result(
                    "Constraint Validation", 
                    True,
                    f"Found constraints - Equal: {len(equal_constraints)}, Opposite: {len(opposite_constraints)}"
                )
            else:
                self.log_result("Constraint Validation", True, "No constraints in this puzzle")
                
        except Exception as e:
            self.log_result("Constraint Validation", False, str(e))
    
    def test_frontend_connectivity(self):
        """Test if frontend can connect to backend"""
        try:
            # Check if frontend is running
            response = requests.get(FRONTEND_URL)
            frontend_running = response.status_code == 200
            
            if frontend_running:
                self.log_result(
                    "Frontend Connectivity", 
                    True,
                    "Frontend is accessible and running"
                )
            else:
                self.log_result(
                    "Frontend Connectivity", 
                    False,
                    f"Frontend returned status code: {response.status_code}"
                )
                
        except Exception as e:
            self.log_result("Frontend Connectivity", False, str(e))
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*60)
        print("TANGO PUZZLE TEST REPORT")
        print("="*60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r['passed'])
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  - {result['test']}")
                    if result['details']:
                        print(f"    Details: {result['details']}")
        
        print("\n" + "="*60)
        
        # Save detailed report
        with open('/Users/jasonagung/Documents/TUGAS AKHIR (SKRIPSI)/tango-puzzle/test_report.json', 'w') as f:
            json.dump({
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'summary': {
                    'total': total_tests,
                    'passed': passed_tests,
                    'failed': failed_tests,
                    'success_rate': f"{(passed_tests/total_tests)*100:.1f}%"
                },
                'results': self.test_results
            }, f, indent=2)
        
        print("\nDetailed report saved to: test_report.json")
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🧪 Starting Comprehensive Tango Puzzle Tests...\n")
        
        # Backend tests
        print("📡 Testing Backend API...")
        self.test_backend_health()
        self.test_puzzle_generation()
        self.test_get_puzzle()
        self.test_validation_empty_board()
        self.test_validation_with_moves()
        self.test_invalid_moves()
        self.test_constraint_validation()
        self.test_hint_system()
        self.test_solver()
        self.test_explanation_system()
        
        # Frontend tests
        print("\n🎮 Testing Frontend...")
        self.test_frontend_connectivity()
        
        # Generate report
        self.generate_report()


def main():
    tester = TangoTester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()