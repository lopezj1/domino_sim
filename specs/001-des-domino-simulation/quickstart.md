# Quick Start Guide: DES Domino Simulation Webapp

**For**: Developers | **Time to First Run**: ~15 minutes

---

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend)
- npm or yarn
- Git

---

## Step 1: Clone & Setup Backend

### 1a. Create Python Virtual Environment

```bash
cd /home/jlopez/domino_sim
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 1b. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Expected output**:
```
Successfully installed fastapi uvicorn pytest ...
```

### 1c. Run Backend Tests

```bash
pytest tests/ -v
```

**Expected output**:
```
tests/unit/test_tile.py::test_tile_creation PASSED
tests/unit/test_game_state.py::test_game_state_initial PASSED
...
======================== XX passed in Xs =======================
```

### 1d. Start Backend Dev Server

```bash
uvicorn src.api.main:app --reload --port 8000
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
pytest tests/unit/test_strategies.py -v -k my_strategy
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
pytest tests/ -v                    # All tests
pytest tests/unit/ -v               # Unit tests only
pytest tests/integration/ -v        # Integration tests only
pytest tests/unit/test_game.py -v   # Specific test file
```

Frontend:
```bash
npm test                            # All tests
npm test -- GameSimulator           # Specific component
```

#### View API Documentation

FastAPI provides interactive docs:
```
http://localhost:8000/docs      # Swagger UI
http://localhost:8000/redoc     # ReDoc
```

---

## Troubleshooting

### Backend won't start
```
Error: Port 8000 already in use
```
Solution: Kill process or use different port:
```bash
uvicorn src.api.main:app --reload --port 8001
```

### Frontend can't reach backend
```
Error: Failed to fetch from http://localhost:8000
```
Solution: Ensure backend is running (Step 1d) and check CORS settings in `backend/src/api/main.py`

### Tests fail with import errors
```
ModuleNotFoundError: No module named 'src'
```
Solution: Ensure you're in `backend/` directory and running from there:
```bash
cd backend
pytest tests/ -v
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
├── src/
│   ├── models/           # Tile, GameState, Move, etc.
│   ├── engine/           # Game simulation core
│   ├── strategy/         # Player strategies
│   ├── simulation/       # Single game + Monte Carlo runners
│   ├── aggregation/      # Statistics
│   └── api/              # FastAPI routes
├── tests/                # Unit + integration tests
└── requirements.txt      # Python deps

frontend/
├── src/
│   ├── components/       # React components
│   ├── pages/            # Page layouts
│   ├── services/         # API client
│   └── hooks/            # Custom React hooks
├── tests/                # Component + E2E tests
└── package.json          # Node deps
```

---

## Next Steps

- **Contribute**: Add more strategies, improve UI, optimize performance
- **Deploy**: See [DEPLOYMENT.md](../docs/DEPLOYMENT.md) for cloud deployment
- **Research**: Export results and analyze using SymPy, scipy, or pandas
- **Extend**: Add 3+ player support, persistent storage, user accounts

---

## Support

For issues or questions:
1. Check existing GitHub issues
2. Review [ARCHITECTURE.md](../docs/ARCHITECTURE.md)
3. Run with `--debug` flag for verbose logs

---

**Happy simulating!** 🎲

Version: 1.0.0 | Last Updated: 2025-01-29
