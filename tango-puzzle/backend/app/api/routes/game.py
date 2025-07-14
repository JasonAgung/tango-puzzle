from fastapi import APIRouter, HTTPException
from typing import Dict
from app.api.models.puzzle import GameState

router = APIRouter()


@router.post("/save", response_model=Dict[str, str])
async def save_game_state(game_state: GameState):
    """Save current game state"""
    # TODO: Implement game state saving
    return {"message": "Game state saved", "id": "temp-save-id"}


@router.get("/load/{save_id}", response_model=GameState)
async def load_game_state(save_id: str):
    """Load a saved game state"""
    # TODO: Implement game state loading
    raise HTTPException(status_code=404, detail="Save not found")