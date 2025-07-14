#!/bin/bash
echo "Starting Tango Puzzle Backend..."
cd backend
uvicorn app.main:app --reload