from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes import puzzle, solver, game

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include routers
app.include_router(puzzle.router, prefix=f"{settings.API_V1_STR}/puzzle", tags=["puzzle"])
app.include_router(solver.router, prefix=f"{settings.API_V1_STR}/solver", tags=["solver"])
app.include_router(game.router, prefix=f"{settings.API_V1_STR}/game", tags=["game"])


@app.get("/")
async def root():
    return {"message": "Welcome to Tango Puzzle API"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}