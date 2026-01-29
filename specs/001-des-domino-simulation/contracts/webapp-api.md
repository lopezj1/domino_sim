# REST API Contracts: DES Domino Simulation Webapp

**Version**: 1.0.0 | **Format**: OpenAPI 3.0

## Base URL
```
http://localhost:8000/api
```

---

## Endpoints

### 1. GET /health

Health check endpoint.

**Request**: None

**Response** (200 OK):
```json
{
  "status": "ok",
  "version": "1.0.0",
  "uptime_seconds": 3600
}
```

---

### 2. GET /strategies

List all available player strategies.

**Request**: None

**Response** (200 OK):
```json
{
  "strategies": [
    {
      "name": "greedy",
      "description": "Plays highest pip tile to reduce hand size"
    },
    {
      "name": "random",
      "description": "Plays random legal move"
    },
    {
      "name": "blocking",
      "description": "Blocks opponent by playing largest tile"
    }
  ]
}
```

---

### 3. POST /game/run

Run a single game between two strategies with a given seed.

**Request**:
```json
{
  "strategy_a": "greedy",
  "strategy_b": "random",
  "seed": 42,
  "include_trace": true
}
```

**Response** (200 OK):
```json
{
  "outcome": {
    "winner": "greedy",
    "score_differential": 15,
    "turns": 47,
    "seed": 42,
    "timestamp": "2025-01-29T16:25:25Z"
  },
  "trace": [
    {
      "type": "deal",
      "timestamp": 0,
      "data": {
        "player_0_hand": [
          {"pips_a": 6, "pips_b": 5},
          {"pips_a": 3, "pips_b": 1}
        ],
        "player_1_hand": [...],
        "boneyard_size": 14
      }
    },
    {
      "type": "play",
      "timestamp": 1,
      "data": {
        "player": 0,
        "tile": {"pips_a": 6, "pips_b": 4}
      }
    },
    ...
  ]
}
```

**Error** (400 Bad Request):
```json
{
  "error": "Invalid strategy name",
  "detail": "Strategy 'unknown' not found"
}
```

---

### 4. POST /monte-carlo/compare

Run multiple paired games and aggregate results.

**Request**:
```json
{
  "strategy_a": "greedy",
  "strategy_b": "random",
  "num_runs": 100,
  "start_seed": 1000
}
```

**Response** (200 OK, long-running):
```json
{
  "result": {
    "strategy_a": "greedy",
    "strategy_b": "random",
    "total_runs": 100,
    "runs_a_wins": 72,
    "runs_b_wins": 28,
    "win_rate_a": 0.72,
    "win_rate_b": 0.28,
    "mean_score_diff_a": 12.34,
    "std_dev_score_diff_a": 8.92,
    "ci_lower": 0.63,
    "ci_upper": 0.81,
    "execution_time_seconds": 45.2
  },
  "per_run_outcomes": [
    {
      "winner": "greedy",
      "score_differential": 5,
      "turns": 32,
      "seed": 1000,
      "timestamp": "2025-01-29T16:25:30Z"
    },
    ...
  ]
}
```

**Error** (400 Bad Request):
```json
{
  "error": "Invalid parameter",
  "detail": "num_runs must be between 10 and 100000"
}
```

---

### 5. POST /monte-carlo/async-compare

Async variant of `/monte-carlo/compare` (returns job ID, use polling to check status).

**Request**:
```json
{
  "strategy_a": "greedy",
  "strategy_b": "random",
  "num_runs": 10000,
  "start_seed": 1000
}
```

**Response** (202 Accepted):
```json
{
  "job_id": "uuid-here",
  "status": "queued"
}
```

---

### 6. GET /monte-carlo/async-compare/{job_id}

Check status of async Monte Carlo job.

**Request**: None (URL param: job_id)

**Response** (200 OK, in-progress):
```json
{
  "job_id": "uuid-here",
  "status": "running",
  "progress": {
    "completed_runs": 2500,
    "total_runs": 10000,
    "percent": 25
  }
}
```

**Response** (200 OK, completed):
```json
{
  "job_id": "uuid-here",
  "status": "completed",
  "result": {
    "strategy_a": "greedy",
    "strategy_b": "random",
    "total_runs": 10000,
    ...
  }
}
```

---

## Request/Response Schemas

### GameOutcome
```json
{
  "winner": "string",               // Strategy name
  "score_differential": "integer",  // >= 0
  "turns": "integer",               // >= 1
  "seed": "integer",
  "timestamp": "string (ISO 8601)"
}
```

### MonteCarloResult
```json
{
  "strategy_a": "string",
  "strategy_b": "string",
  "total_runs": "integer (>= 10)",
  "runs_a_wins": "integer",
  "runs_b_wins": "integer",
  "win_rate_a": "number (0.0-1.0)",
  "win_rate_b": "number (0.0-1.0)",
  "mean_score_diff_a": "number",
  "std_dev_score_diff_a": "number",
  "ci_lower": "number",
  "ci_upper": "number",
  "execution_time_seconds": "number"
}
```

### Event
```json
{
  "type": "enum(deal, play, draw, pass, round_end, game_end)",
  "timestamp": "integer (>= 0)",
  "data": "object"
}
```

---

## Error Codes

| Code | Message | Cause |
|------|---------|-------|
| 400 | Bad Request | Invalid strategy name, out-of-range parameters |
| 404 | Not Found | Job ID not found (async endpoints) |
| 500 | Internal Server Error | Simulation engine crash |
| 503 | Service Unavailable | Too many concurrent jobs |

---

## Rate Limiting

No rate limiting for MVP. Can add in future if needed.

---

## CORS

Allow-Origin: * (or specify frontend domain)

---

**Version**: 1.0.0 | **Status**: Ready for Implementation
