# How to Run Tango Puzzle Game

## Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- npm or yarn

## Step 1: Start the Backend Server

1. Open a terminal and navigate to the backend directory:
```bash
cd /Users/jasonagung/Documents/TUGAS\ AKHIR\ \(SKRIPSI\)/tango-puzzle/backend
```

2. Install Python dependencies (if not already installed):
```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The backend should now be running at http://localhost:8000
You can check the API documentation at http://localhost:8000/docs

## Step 2: Start the Frontend

1. Open a NEW terminal window/tab and navigate to the frontend directory:
```bash
cd /Users/jasonagung/Documents/TUGAS\ AKHIR\ \(SKRIPSI\)/tango-puzzle/frontend
```

2. Install dependencies (if not already installed):
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend should now be running at http://localhost:5173

## Step 3: Play the Game

1. Open your web browser and go to http://localhost:5173
2. The game will automatically load a new puzzle
3. Click cells to place suns (☀️) or moons (🌙)
4. Use the controls on the right to:
   - Change difficulty
   - Get hints
   - Reset or solve the puzzle

## Troubleshooting

### If the backend fails to start:
- Make sure you're in the correct directory
- Check that Python dependencies are installed
- Ensure port 8000 is not in use

### If the frontend fails to start:
- Make sure you're in the correct directory
- Check that npm dependencies are installed
- Ensure port 5173 is not in use

### If the game doesn't load puzzles:
- Check that the backend is running
- Check browser console for errors
- Ensure both servers are running on correct ports