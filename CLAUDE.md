# Tango Logic Puzzle Game Project

## Project Overview
This is a final project (Tugas Akhir/Skripsi) for developing a Tango logic puzzle game and its solver.

## Game Rules
The Tango puzzle (also known as Tangly) is a visual logic game with the following rules:

1. **Grid**: 6×6 grid where each cell must be filled with either a sun (matahari) or moon (bulan) symbol
   - In the reference, it mentions blueberries and lemons as alternative symbols

2. **Distribution**: Each row and column must contain exactly 3 suns and 3 moons

3. **No Repetition**: No more than 2 of the same symbol may be placed consecutively (horizontally or vertically)

4. **Special Symbols**:
   - **Equal sign (=)**: Cells separated by = must contain the same symbol
   - **Cross sign (×)**: Cells separated by × must contain opposite symbols

5. **Solving Method**: Each puzzle has one unique solution and can be solved through logical deduction without guessing

## Project Objectives
The student must:
1. Study how to solve Tango puzzles by playing at https://www.tangly.org
2. Learn solving strategies for Tango puzzles
3. Analyze and design:
   - The Tango game software
   - A solver/solution finder for Tango puzzles
4. Build the game software and its solver
5. Perform testing, including comparing manual solutions with computer-generated solutions

## References
1. **O'Sullivan & Horan**: Research on generating and solving logic puzzles through constraint satisfaction, focusing on Jidoku (Less-Than-Sudoku) which uses constraint satisfaction techniques including:
   - Problem formulation with CSP
   - Global constraints (alldifferent)
   - Search and inference procedures
   - Puzzle minimization for difficulty control
   - Ensuring unique solutions and solvability through logic alone

2. **Bogaerts et al.**: Framework for step-wise explaining how to solve constraint satisfaction problems, emphasizing:
   - Explainable AI for constraint solvers
   - Creating human-interpretable explanations
   - Step-by-step solution explanations
   - Focus on cognitive simplicity for humans
   - Complete and interpretable explanation sequences

## Technical Approach
Based on the references, the project should implement:
- Constraint Satisfaction Problem (CSP) formulation
- Propagation and inference mechanisms
- Unique solution guarantee
- Difficulty grading
- Step-by-step explanations for solutions

## Project Structure (Web-Based Implementation)

```
tango-puzzle/
├── frontend/                    # React.js frontend application
│   ├── public/
│   │   ├── index.html
│   │   └── assets/             # Images for sun/moon symbols
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameBoard/
│   │   │   │   ├── GameBoard.jsx
│   │   │   │   ├── Cell.jsx
│   │   │   │   ├── Constraint.jsx
│   │   │   │   └── GameBoard.css
│   │   │   ├── Controls/
│   │   │   │   ├── Controls.jsx
│   │   │   │   ├── DifficultySelector.jsx
│   │   │   │   └── GameTimer.jsx
│   │   │   ├── SolutionViewer/
│   │   │   │   ├── SolutionViewer.jsx
│   │   │   │   ├── StepExplanation.jsx
│   │   │   │   └── SolutionViewer.css
│   │   │   └── UI/
│   │   │       ├── Button.jsx
│   │   │       ├── Modal.jsx
│   │   │       └── Toast.jsx
│   │   ├── hooks/
│   │   │   ├── useGameState.js
│   │   │   ├── useSolver.js
│   │   │   └── useTimer.js
│   │   ├── services/
│   │   │   ├── api.js          # API calls to backend
│   │   │   └── gameLogic.js    # Client-side game logic
│   │   ├── utils/
│   │   │   ├── constants.js
│   │   │   └── helpers.js
│   │   ├── styles/
│   │   │   └── global.css
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── .env
│
├── backend/                     # Python Flask/FastAPI backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py             # FastAPI app entry point
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── puzzle.py   # Puzzle generation endpoints
│   │   │   │   ├── solver.py   # Solver endpoints
│   │   │   │   └── game.py     # Game state endpoints
│   │   │   └── models/
│   │   │       ├── __init__.py
│   │   │       ├── puzzle.py   # Pydantic models
│   │   │       └── solution.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── puzzle_generator.py
│   │   │   ├── csp_solver.py
│   │   │   ├── constraint_validator.py
│   │   │   ├── explanation_engine.py
│   │   │   └── difficulty_analyzer.py
│   │   ├── solver/
│   │   │   ├── __init__.py
│   │   │   ├── constraints.py  # CSP constraint definitions
│   │   │   ├── propagator.py   # Constraint propagation
│   │   │   ├── search.py       # Search algorithms
│   │   │   └── inference_rules.py
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   └── helpers.py
│   │   └── config.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_generator.py
│   │   ├── test_solver.py
│   │   ├── test_constraints.py
│   │   └── fixtures/
│   │       └── sample_puzzles.json
│   ├── requirements.txt
│   └── .env
│
├── database/                    # Optional: for storing puzzles/scores
│   └── schema.sql
│
├── docs/                        # Documentation
│   ├── API.md
│   ├── SOLVER_ALGORITHM.md
│   └── USER_GUIDE.md
│
├── scripts/                     # Utility scripts
│   ├── generate_puzzles.py
│   └── validate_solutions.py
│
├── docker-compose.yml          # For containerization
├── README.md
└── .gitignore
```

## Technology Stack Details

### Frontend:
- **React.js 18+** with functional components and hooks
- **Axios** for API communication
- **CSS Modules** or **Styled Components** for styling
- **React Context API** for state management
- **Vite** as build tool (faster than Create React App)

### Backend:
- **FastAPI** (Python) - modern, fast, with automatic API documentation
- **Python-constraint** or **OR-Tools** for CSP solving
- **Pydantic** for data validation
- **CORS middleware** for frontend communication
- **Uvicorn** as ASGI server

### Development Tools:
- **ESLint** and **Prettier** for frontend code quality
- **Black** and **Flake8** for Python code formatting
- **Jest** and **React Testing Library** for frontend tests
- **Pytest** for backend tests
- **Git** for version control

## API Endpoints Design

```
POST   /api/puzzle/generate      # Generate new puzzle
GET    /api/puzzle/{id}          # Get specific puzzle
POST   /api/puzzle/validate      # Validate current board state
POST   /api/solver/solve         # Get complete solution
POST   /api/solver/hint          # Get next logical move
POST   /api/solver/explain       # Get step-by-step explanation
GET    /api/solver/check         # Check if current state is solvable
```

## Key Implementation Notes

1. **Separation of Concerns**: Frontend handles UI/UX, backend handles all game logic and solving
2. **Real-time Validation**: Frontend sends board state to backend for validation
3. **Progressive Hints**: Solver can provide hints without revealing entire solution
4. **Explanation System**: Each solver step includes human-readable explanation
5. **Performance**: Cache generated puzzles, use WebSocket for real-time features if needed

## Implementation Details

### CSP Solver Algorithm
The solver uses a combination of constraint propagation and search:

1. **Arc Consistency (AC-3)**:
   - Maintains consistency between all pairs of constrained variables
   - Reduces domains by eliminating impossible values
   - Runs after each assignment to prune search space

2. **Inference Rules**:
   - **Row/Column Completion**: If a row has 3 suns, remaining cells must be moons
   - **Consecutive Prevention**: If two adjacent cells have same symbol, third must be different
   - **Constraint Propagation**: Equal/cross constraints immediately determine related cells
   - **Counting Logic**: Track remaining symbols needed per row/column

3. **Search Strategy**:
   - **MRV (Minimum Remaining Values)**: Choose cell with fewest legal values
   - **Forward Checking**: Eliminate values that violate constraints
   - **Backtracking**: Undo assignments when contradictions found
   - **Solution Uniqueness Check**: Verify no other solutions exist

### Puzzle Generation Algorithm

1. **Initial Generation**:
   ```python
   def generate_puzzle(difficulty):
       # Start with empty grid
       grid = create_empty_grid(6, 6)
       
       # Add random valid assignments (seeds)
       add_random_seeds(grid, seed_count=difficulty_seeds[difficulty])
       
       # Use solver to complete grid
       solution = csp_solver.solve(grid)
       
       # Strategically remove cells while maintaining uniqueness
       puzzle = minimize_puzzle(solution, difficulty)
       
       # Add constraint symbols
       add_constraints(puzzle, difficulty)
       
       return puzzle
   ```

2. **Difficulty Levels**:
   - **Easy**: More given cells (18-22), basic constraints only
   - **Medium**: Fewer given cells (12-17), mix of = and × constraints
   - **Hard**: Minimal given cells (8-11), complex constraint patterns

3. **Uniqueness Guarantee**:
   - After each cell removal, verify solution remains unique
   - Use solution counting algorithm to ensure exactly one solution
   - Rollback removal if multiple solutions possible

### Frontend State Management

```javascript
// Game state structure
const gameState = {
  grid: Array(6).fill(Array(6).fill(null)), // null | 'sun' | 'moon'
  constraints: {
    horizontal: [], // Array of constraint objects
    vertical: []    // Array of constraint objects
  },
  history: [],      // Undo/redo stack
  hints: [],        // Available hints
  timer: 0,         // Game timer in seconds
  difficulty: 'medium',
  isComplete: false,
  errors: []        // Current constraint violations
};

// Context provider for global state
const GameContext = createContext();

// Custom hook for game logic
const useGameLogic = () => {
  const [state, dispatch] = useReducer(gameReducer, initialState);
  
  const placeSynbol = (row, col, symbol) => {
    dispatch({ type: 'PLACE_SYMBOL', payload: { row, col, symbol } });
    validateBoard();
  };
  
  // Other game actions...
};
```

### Backend Architecture Patterns

1. **Repository Pattern** for data access:
   ```python
   class PuzzleRepository:
       def create(self, puzzle: Puzzle) -> Puzzle
       def get_by_id(self, puzzle_id: str) -> Optional[Puzzle]
       def get_by_difficulty(self, difficulty: str) -> List[Puzzle]
   ```

2. **Service Layer** for business logic:
   ```python
   class SolverService:
       def solve(self, puzzle: PuzzleGrid) -> Solution
       def get_hint(self, current_state: GameState) -> Hint
       def validate(self, grid: PuzzleGrid) -> ValidationResult
   ```

3. **Dependency Injection** for testability:
   ```python
   def get_solver_service(
       repo: PuzzleRepository = Depends(get_repository),
       solver: CSPSolver = Depends(get_solver)
   ) -> SolverService:
       return SolverService(repo, solver)
   ```

### Testing Strategies

1. **Unit Tests**:
   - Test each constraint type individually
   - Verify solver produces correct solutions
   - Test puzzle generation maintains uniqueness

2. **Integration Tests**:
   - Test API endpoints with various inputs
   - Verify frontend-backend communication
   - Test complete game flows

3. **Property-Based Testing**:
   - All generated puzzles must have unique solutions
   - All solutions must satisfy all constraints
   - Solver must find solution for any valid puzzle

4. **Performance Benchmarks**:
   - Solver should complete within 1 second for any puzzle
   - API response times under 100ms for validation
   - Frontend renders at 60 FPS during interactions

### Deployment Configuration

```yaml
# docker-compose.yml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://backend:8000
    
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/tango
      - REDIS_URL=redis://redis:6379
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - frontend
      - backend
```

### Security Considerations

1. **Input Validation**: Validate all puzzle inputs on backend
2. **Rate Limiting**: Limit API calls to prevent abuse
3. **CORS Configuration**: Restrict origins in production
4. **Environment Variables**: Never commit secrets
5. **SQL Injection Prevention**: Use parameterized queries
6. **XSS Protection**: Sanitize user inputs in frontend