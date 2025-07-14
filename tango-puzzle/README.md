# Tango Logic Puzzle Game

A web-based implementation of the Tango (Tangly) logic puzzle game with an intelligent solver using Constraint Satisfaction Problem (CSP) techniques.

## 🎮 Game Overview

Tango is a visual logic puzzle where players must fill a 6×6 grid with sun ☀️ and moon 🌙 symbols following specific rules:

- Each row and column must contain exactly 3 suns and 3 moons
- No more than 2 of the same symbol may appear consecutively (horizontally or vertically)
- Cells connected by = must contain the same symbol
- Cells connected by × must contain opposite symbols
- Each puzzle has one unique solution solvable through logical deduction

## 🚀 Features

- **Interactive Gameplay**: Click to cycle through sun, moon, or empty cells
- **Multiple Difficulty Levels**: Easy, Medium, and Hard puzzles
- **Intelligent Solver**: CSP-based solver with step-by-step explanations
- **Hint System**: Get logical hints without revealing the entire solution
- **Real-time Validation**: Immediate feedback on constraint violations
- **Timer**: Track your solving time
- **Responsive Design**: Works on desktop and mobile devices

## 🛠️ Technology Stack

### Frontend
- React 18+ with Vite
- CSS Modules for styling
- Axios for API communication
- React hooks for state management

### Backend
- FastAPI (Python)
- OR-Tools for constraint satisfaction
- Pydantic for data validation
- Uvicorn ASGI server

## 📦 Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

4. Open http://localhost:5173 in your browser

## 🎯 Quick Start

### Using the provided scripts:

1. Start the backend:
```bash
./scripts/start-backend.sh
```

2. Start the frontend:
```bash
./scripts/start-frontend.sh
```

### Using the launcher script:
```bash
python run_game.py
```

## 🧩 How to Play

1. **Select Difficulty**: Choose from Easy, Medium, or Hard
2. **Place Symbols**: Click cells to cycle through: empty → sun → moon → empty
3. **Follow the Rules**: 
   - Each row/column needs 3 suns and 3 moons
   - Avoid 3 consecutive identical symbols
   - Respect = (same) and × (different) constraints
4. **Use Hints**: Click "Get Hint" if you're stuck
5. **Complete the Puzzle**: Fill all cells correctly to win!

## 🔧 API Documentation

### Endpoints

- `POST /api/puzzle/generate` - Generate a new puzzle
- `GET /api/puzzle/{id}` - Get a specific puzzle
- `POST /api/puzzle/validate` - Validate current board state
- `POST /api/solver/solve` - Get complete solution
- `POST /api/solver/hint` - Get next logical move
- `POST /api/solver/explain` - Get step-by-step explanation

## 🧪 Testing

### Run all tests:
```bash
python tests/comprehensive_test.py
```

### Run specific test suites:
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## 📂 Project Structure

```
tango-puzzle/
├── frontend/                # React frontend application
│   ├── src/
│   │   ├── components/     # UI components
│   │   ├── hooks/          # Custom React hooks
│   │   ├── services/       # API services
│   │   └── utils/          # Utility functions
│   └── public/             # Static assets
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/           # API routes and models
│   │   ├── core/          # Core game logic
│   │   └── solver/        # CSP solver implementation
│   └── tests/             # Backend tests
├── scripts/                # Utility scripts
├── tests/                  # Integration tests
└── docs/                   # Additional documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Jason Agung**  
Final Year Project (Tugas Akhir/Skripsi)

## 🙏 Acknowledgments

- Based on the Tangly puzzle from [tangly.org](https://www.tangly.org)
- CSP solving techniques inspired by O'Sullivan & Horan's research
- Explanation system based on Bogaerts et al.'s framework

## 📚 References

1. O'Sullivan, B., & Horan, J. - "Generating and Solving Logic Puzzles through Constraint Satisfaction"
2. Bogaerts, B., et al. - "Step-wise Explaining How to Solve Constraint Satisfaction Problems"

---

For more detailed information, see the [documentation](docs/) directory.