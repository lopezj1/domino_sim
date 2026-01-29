# Quick Start Guide: DES Domino Simulation Webapp

**For**: Developers | **Time to First Run**: ~15 minutes

---

## Prerequisites

- **Python 3.11+** installed on your system
- **uv** package manager ([install uv](https://astral.sh/uv/install.sh))
- **Node.js 18+** (for frontend)
- **npm** or **yarn**
- **Git**

---

## Step 1: Clone & Setup Backend (with uv)

### 1a. Install uv (one-time)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Verify: uv --version
```

### 1b. Create Python Virtual Environment

```bash
cd /home/jlopez/domino_sim/backend

# Create virtual environment with uv
uv venv .venv

# Activate the environment
source .venv/bin/activate
# On Windows: .venv\Scripts\activate
```

### 1c. Install Python Dependencies

```bash
# Sync dependencies from uv.lock (locked versions for reproducibility)
uv sync

# Verify installation
python --version  # Should be 3.11+
pytest --version
```

**Expected output**:
```
Successfully synced dependencies from uv.lock
```

### 1d. Run Backend Tests

```bash
cd /home/jlopez/domino_sim/backend
uv run pytest tests/ -v
```

**Expected output**:
```
tests/unit/test_tile.py::test_tile_creation PASSED
tests/unit/test_game_state.py::test_game_state_initial PASSED
...
======================== XX passed in Xs =======================
```

### 1e. Start Backend Dev Server

```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

**Expected output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

The backend is now running. You can test it:

```bash
curl http://localhost:8000/api/health
# {"status":"ok","version":"1.0.0"}
```

---

## Step 2: Setup & Run Frontend

### 2a. Install Node Dependencies

```bash
cd ../frontend
npm install
```

**Expected output**:
```
added XXX packages in Xs
```

### 2b. Start Frontend Dev Server

```bash
npm run dev
```

**Expected output**:
```
  VITE v4.x.x  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### 2c. Open in Browser

Open http://localhost:5173 in your browser. You should see:
- Home page with "Single Game" and "Compare Strategies" buttons
- Links to available strategies

---

## Step 3: Run Your First Simulation

### 3a. Single Game (via UI)

1. Click "Single Game Simulator"
2. Select:
   - Strategy A: "greedy"
   - Strategy B: "random"
   - Seed: "12345"
3. Click "Run Game"
4. See result: winner, score differential, move history

### 3b. Single Game (via API)

```bash
curl -X POST http://localhost:8000/api/game/run \
  -H "Content-Type: application/json" \
  -d '{
    "strategy_a": "greedy",
    "strategy_b": "random",
    "seed": 12345,
    "include_trace": false
  }'
```

Response:
```json
{
  "outcome": {
    "winner": "greedy",
    "score_differential": 18,
    "turns": 52,
    "seed": 12345,
    "timestamp": "2025-01-29T16:30:00Z"
  }
}
```

---

## Step 4: Run Monte Carlo Comparison

### 4a. Via UI

1. Click "Strategy Comparison"
2. Select:
   - Strategy A: "greedy"
   - Strategy B: "blocking"
   - Num Runs: "100"
3. Click "Compare"
4. Wait 30-60 seconds
5. See charts: win rate, confidence interval, score differential
6. Click "Export" to download JSON

### 4b. Via API

```bash
curl -X POST http://localhost:8000/api/monte-carlo/compare \
  -H "Content-Type: application/json" \
  -d '{
    "strategy_a": "greedy",
    "strategy_b": "blocking",
    "num_runs": 50,
    "start_seed": 1000
  }'
```

Response:
```json
{
  "result": {
    "strategy_a": "greedy",
    "strategy_b": "blocking",
    "total_runs": 50,
    "runs_a_wins": 34,
    "runs_b_wins": 16,
    "win_rate_a": 0.68,
    "mean_score_diff_a": 11.5,
    "ci_lower": 0.55,
    "ci_upper": 0.81,
    "execution_time_seconds": 15.2
  },
  "per_run_outcomes": [...]
}
```

---

## Step 5: Explore & Develop

### Common Tasks

#### Add a New Strategy

1. Create `backend/src/strategy/my_strategy.py`:

```python
from src.strategy.base import Strategy
from src.models.game_state import GameState
from src.models.move import Move

class MyStrategy(Strategy):
    @property
    def name(self) -> str:
        return "my_strategy"
    
    def choose_move(self, state: GameState, legal_moves: list[Move]) -> Move:
        """My custom strategy logic."""
        # Choose the move with highest total pips
        return max(legal_moves, key=lambda m: m.tile.total_pips if m.tile else 0)
```

2. Register in `backend/src/api/routes/strategies.py`:

```python
from src.strategy.my_strategy import MyStrategy

AVAILABLE_STRATEGIES = {
    "greedy": GreedyStrategy(),
    "random": RandomStrategy(),
    "blocking": BlockingStrategy(),
    "my_strategy": MyStrategy(),  # Add this
}
```

3. Test:
```bash
cd backend
uv run pytest tests/unit/test_strategies.py -v -k my_strategy
```

4. Use in UI: Strategy selectors now include "my_strategy"

#### Add a New API Endpoint

1. Create `backend/src/api/routes/my_endpoint.py`:

```python
from fastapi import APIRouter, HTTPException
from src.models.game_state import GameState

router = APIRouter(prefix="/api")

@router.get("/my-endpoint")
def my_endpoint():
    """My new endpoint."""
    return {"message": "Hello"}
```

2. Register in `backend/src/api/main.py`:

```python
from src.api.routes import my_endpoint

app.include_router(my_endpoint.router)
```

3. Test:
```bash
curl http://localhost:8000/api/my-endpoint
```

#### Run Tests

Backend:
```bash
cd backend
uv run pytest tests/ -v                    # All tests
uv run pytest tests/unit/ -v               # Unit tests only
uv run pytest tests/integration/ -v        # Integration tests only
uv run pytest tests/unit/test_game.py -v   # Specific test file
```

Frontend:
```bash
cd frontend
npm test                            # All tests
npm test -- GameSimulator           # Specific component
```

#### Format & Lint Code

```bash
cd backend

# Format with Black
uv run black src/ tests/

# Sort imports with isort
uv run isort src/ tests/

# Lint with flake8
uv run flake8 src/ tests/

# Type check with mypy
uv run mypy src/
```

#### View API Documentation

FastAPI provides interactive docs:
```
http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc
```

---

## Common uv Commands

| Task | Command |
|------|---------|
| **Create env** | `uv venv .venv` |
| **Activate env** | `source .venv/bin/activate` |
| **Sync deps** | `uv sync` |
| **Run tests** | `uv run pytest` |
| **Format** | `uv run black src/` |
| **Add dep** | `uv add package-name` |

---

## Troubleshooting

### Backend won't start
```
Error: Port 8000 already in use
```
Solution: Kill process or use different port:
```bash
uv run uvicorn src.api.main:app --reload --port 8001
```

### Frontend can't reach backend
```
Error: Failed to fetch from http://localhost:8000
```
Solution: Ensure backend is running (Step 1e) and check CORS settings in `backend/src/api/main.py`

### Tests fail with import errors
```
ModuleNotFoundError: No module named 'src'
```
Solution: Ensure you're in `backend/` directory and running with uv:
```bash
cd backend
uv run pytest tests/ -v
```

### Virtual environment issues
```bash
# Recreate from scratch
rm -rf .venv/
uv venv .venv
source .venv/bin/activate
uv sync
```

### Node/Python version issues
```
Error: Node.js version too old
```
Solution:
```bash
node --version    # Ensure >= 18.0.0
python3 --version # Ensure >= 3.11
```

---

## File Structure Reference

```
backend/
├── pyproject.toml        # uv project config
├── uv.lock              # Locked dependency versions
├── .venv/               # Virtual environment (created by uv)
├── src/
│   ├── models/          # Tile, GameState, Move, etc.
│   ├── engine/          # Game simulation core
│   ├── strategy/        # Player strategies
│   ├── simulation/      # Single game + Monte Carlo runners
│   ├── aggregation/     # Statistics
│   └── api/             # FastAPI routes
└── tests/               # Unit + integration tests

frontend/
├── src/
│   ├── components/      # React components
│   ├── pages/           # Page layouts
│   ├── services/        # API client
│   └── hooks/           # Custom React hooks
└── tests/               # Component + E2E tests
```

---

## Next Steps

- **Run tests**: `cd backend && uv run pytest` to verify everything works
- **Explore code**: Check `backend/src/models/` to understand game state
- **Add strategies**: Implement your own strategy in `backend/src/strategy/`
- **Extend features**: Build on the simulation engine for new game modes
- **Deploy**: See DEPLOYMENT.md for production setup

---

## Support

For issues or questions:
1. Check existing GitHub issues
2. Review ARCHITECTURE.md
3. Run with `--debug` flag for verbose logs

---

**Happy simulating!** 🎲

Version: 1.0.0 | Last Updated: 2025-01-29 | Using uv for environment management
