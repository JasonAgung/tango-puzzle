#!/usr/bin/env python3
import subprocess
import time
import sys
import os

def test_servers():
    backend_process = None
    frontend_process = None
    
    try:
        # Start backend
        print("Starting backend server...")
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        backend_process = subprocess.Popen(
            [sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload', '--host', '127.0.0.1', '--port', '8000'],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for backend to start
        time.sleep(3)
        
        # Start frontend
        print("Starting frontend server...")
        frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
        frontend_process = subprocess.Popen(
            ['npm', 'run', 'dev'],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for frontend to start
        time.sleep(3)
        
        print("\n✅ Both servers should be running!")
        print("🌐 Backend: http://localhost:8000")
        print("🌐 Backend API Docs: http://localhost:8000/docs")
        print("🎮 Frontend: http://localhost:5173")
        print("\nPress Ctrl+C to stop both servers...")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nStopping servers...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("Servers stopped.")

if __name__ == "__main__":
    test_servers()