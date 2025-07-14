#!/usr/bin/env python3
"""
Test script to verify difficulty selector functionality
"""
import asyncio
import httpx
import json
from collections import defaultdict

async def test_difficulty_generation():
    """Test if different difficulties generate puzzles with appropriate characteristics"""
    
    base_url = "http://localhost:8000/api/v1"
    difficulties = ["easy", "medium", "hard"]
    samples_per_difficulty = 5
    
    results = defaultdict(list)
    
    async with httpx.AsyncClient() as client:
        for difficulty in difficulties:
            print(f"\nTesting {difficulty} difficulty...")
            
            for i in range(samples_per_difficulty):
                try:
                    # Generate puzzle
                    response = await client.post(
                        f"{base_url}/puzzle/generate",
                        json={"difficulty": difficulty}
                    )
                    
                    if response.status_code == 200:
                        puzzle_data = response.json()
                        
                        # Count given cells (non-null cells)
                        given_count = sum(
                            1 for row in puzzle_data["grid"] 
                            for cell in row if cell is not None
                        )
                        
                        # Count constraints
                        constraint_count = len(puzzle_data["constraints"])
                        
                        results[difficulty].append({
                            "given_cells": given_count,
                            "constraints": constraint_count,
                            "id": puzzle_data["id"]
                        })
                        
                        print(f"  Sample {i+1}: {given_count} given cells, {constraint_count} constraints")
                    else:
                        print(f"  Error: {response.status_code} - {response.text}")
                        
                except Exception as e:
                    print(f"  Error generating puzzle: {e}")
    
    # Analyze results
    print("\n" + "="*50)
    print("DIFFICULTY ANALYSIS RESULTS:")
    print("="*50)
    
    for difficulty in difficulties:
        if results[difficulty]:
            samples = results[difficulty]
            avg_given = sum(s["given_cells"] for s in samples) / len(samples)
            avg_constraints = sum(s["constraints"] for s in samples) / len(samples)
            
            print(f"\n{difficulty.upper()} Difficulty:")
            print(f"  Average given cells: {avg_given:.1f}")
            print(f"  Average constraints: {avg_constraints:.1f}")
            print(f"  Given cells range: {min(s['given_cells'] for s in samples)} - {max(s['given_cells'] for s in samples)}")
            print(f"  Constraints range: {min(s['constraints'] for s in samples)} - {max(s['constraints'] for s in samples)}")
    
    # Check if difficulties are properly differentiated
    print("\n" + "="*50)
    print("DIFFICULTY DIFFERENTIATION CHECK:")
    print("="*50)
    
    if all(results[d] for d in difficulties):
        easy_avg = sum(s["given_cells"] for s in results["easy"]) / len(results["easy"])
        medium_avg = sum(s["given_cells"] for s in results["medium"]) / len(results["medium"])
        hard_avg = sum(s["given_cells"] for s in results["hard"]) / len(results["hard"])
        
        if easy_avg > medium_avg > hard_avg:
            print("✅ Given cells properly decrease with difficulty (Easy > Medium > Hard)")
        else:
            print("❌ Given cells NOT properly differentiated!")
            print(f"   Easy: {easy_avg:.1f}, Medium: {medium_avg:.1f}, Hard: {hard_avg:.1f}")
        
        # Check constraint differentiation
        easy_const = sum(s["constraints"] for s in results["easy"]) / len(results["easy"])
        medium_const = sum(s["constraints"] for s in results["medium"]) / len(results["medium"])
        hard_const = sum(s["constraints"] for s in results["hard"]) / len(results["hard"])
        
        print(f"\nConstraint averages - Easy: {easy_const:.1f}, Medium: {medium_const:.1f}, Hard: {hard_const:.1f}")

if __name__ == "__main__":
    print("Testing Tango Puzzle Difficulty Generation...")
    print("Make sure the backend server is running on http://localhost:8000")
    asyncio.run(test_difficulty_generation())