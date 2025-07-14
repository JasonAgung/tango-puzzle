#!/usr/bin/env python3
"""
Simple script to run both backend and frontend servers
"""
import subprocess
import time
import os
import sys
import webbrowser

def run_servers():
    backend_port = 8000
    frontend_port = 5173
    
    print("🚀 Starting Tango Puzzle Game...")
    print("=" * 50)
    
    # Start backend
    print(f"📦 Starting backend server on port {backend_port}...")
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    backend_cmd = [sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload', '--port', str(backend_port)]
    backend_process = subprocess.Popen(backend_cmd, cwd=backend_dir)
    
    # Wait for backend to start
    time.sleep(3)
    
    # Start frontend
    print(f"🎨 Starting frontend server on port {frontend_port}...")
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    frontend_cmd = ['npm', 'run', 'dev', '--', '--port', str(frontend_port)]
    frontend_process = subprocess.Popen(frontend_cmd, cwd=frontend_dir)
    
    # Wait for frontend to start
    time.sleep(5)
    
    print("\n✅ Game is ready!")
    print(f"🌐 Backend API: http://localhost:{backend_port}/docs")
    print(f"🎮 Play Game: http://localhost:{frontend_port}")
    print("\n📝 Opening game in browser...")
    
    # Open browser
    webbrowser.open(f'http://localhost:{frontend_port}')
    
    print("\n⚠️  Press Ctrl+C to stop the servers")
    
    try:
        # Keep running
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped")

if __name__ == "__main__":
    run_servers()