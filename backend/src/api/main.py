"""FastAPI application for domino simulation."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import game_router, visualization_router

app = FastAPI(
    title="Domino Simulation API",
    description="Discrete Event Simulation for Domino Game with Monte Carlo Strategy Evaluation",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "domino-simulation"}

# Include routers
app.include_router(visualization_router)
app.include_router(game_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
