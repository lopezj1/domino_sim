# Monte Carlo Visualization - Implementation Summary

## What Was Completed

### 1. Specification Updates ✅
- **[spec.md](specs/001-des-domino-simulation/spec.md)**: Added User Story 5 for Monte Carlo visualization
- **[data-model.md](specs/001-des-domino-simulation/data-model.md)**: Added `MonteCarloVisualizationData` entity
- **[plan.md](specs/001-des-domino-simulation/plan.md)**: Updated project structure with visualization components

### 2. Backend Implementation ✅
**Files Created/Modified:**
- `backend/src/aggregation/monte_carlo.py` - Added `generate_visualization_data()` method (95 lines)
- `backend/src/api/schemas/visualization.py` - Pydantic request/response models (NEW)
- `backend/src/api/routes/visualization.py` - API endpoint for visualization data (NEW)
- `backend/src/api/main.py` - FastAPI app with visualization router (NEW)
- `backend/src/api/routes/__init__.py` - Router exports (NEW)

**Tests Created:**
- `backend/tests/unit/test_monte_carlo_visualization.py` - 6 new tests (all passing)

**Test Results:**
```
58 tests passing (52 original + 6 new)
Coverage: 86%
```

### 3. API Endpoints ✅

#### POST `/visualization/monte-carlo-paths`
**Request:**
```json
{
  "strategy_a": "blocking",
  "strategy_b": "random",
  "num_games": 500,
  "num_paths": 100,
  "seed": 12345
}
```

**Response:**
```json
{
  "strategy_a": "blocking",
  "strategy_b": "random",
  "total_games": 500,
  "num_paths": 100,
  "game_numbers": [1, 2, 3, ..., 500],
  "paths": [[0.0, 0.5, 0.67, ...], ...],  // 100 paths
  "final_win_rate_a": 0.578,
  "final_win_rate_b": 0.422,
  "ci_lower": 0.52,
  "ci_upper": 0.64,
  "convergence_std": 0.045
}
```

#### GET `/visualization/strategies`
Returns list of available strategies (greedy, random, blocking)

#### GET `/health`
Health check endpoint

### 4. Server Running ✅
FastAPI server running on `http://127.0.0.1:8001`

---

## Frontend Implementation Guide

### Required Dependencies
```bash
cd frontend
npm install recharts axios @types/recharts
```

### TypeScript Types
Create `frontend/src/services/types.ts`:

```typescript
export interface MonteCarloVisualizationRequest {
  strategy_a: string;
  strategy_b: string;
  num_games: number;
  num_paths: number;
  seed: number;
}

export interface MonteCarloVisualizationResponse {
  strategy_a: string;
  strategy_b: string;
  total_games: number;
  num_paths: number;
  game_numbers: number[];
  paths: number[][];
  final_win_rate_a: number;
  final_win_rate_b: number;
  ci_lower: number;
  ci_upper: number;
  convergence_std: number;
}
```

### API Service
Create `frontend/src/services/api.ts`:

```typescript
import axios from 'axios';
import type { MonteCarloVisualizationRequest, MonteCarloVisualizationResponse } from './types';

const API_BASE = 'http://127.0.0.1:8001';

export const api = {
  async getMonteCarloVisualization(
    request: MonteCarloVisualizationRequest
  ): Promise<MonteCarloVisualizationResponse> {
    const response = await axios.post<MonteCarloVisualizationResponse>(
      `${API_BASE}/visualization/monte-carlo-paths`,
      request
    );
    return response.data;
  },
  
  async getStrategies(): Promise<{ strategies: Array<{ name: string; description: string }> }> {
    const response = await axios.get(`${API_BASE}/visualization/strategies`);
    return response.data;
  }
};
```

### React Component
Create `frontend/src/components/MonteCarloPathsChart.tsx`:

```typescript
import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ReferenceLine,
  ResponsiveContainer
} from 'recharts';
import type { MonteCarloVisualizationResponse } from '../services/types';

interface Props {
  data: MonteCarloVisualizationResponse;
}

export const MonteCarloPathsChart: React.FC<Props> = ({ data }) => {
  // Transform data for Recharts format
  const chartData = data.game_numbers.map((gameNum, idx) => {
    const point: any = { gameNumber: gameNum };
    
    // Add each path as a separate series
    data.paths.forEach((path, pathIdx) => {
      point[`path${pathIdx}`] = path[idx];
    });
    
    return point;
  });

  return (
    <div className="w-full h-[600px] p-4">
      <h3 className="text-xl font-bold mb-4">
        Monte Carlo Convergence: {data.strategy_a} vs {data.strategy_b}
      </h3>
      
      <ResponsiveContainer width="100%" height="90%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="gameNumber"
            label={{ value: 'Game Number', position: 'insideBottom', offset: -5 }}
          />
          <YAxis
            domain={[0, 1]}
            label={{ value: 'Cumulative Win Rate', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip />
          <Legend />
          
          {/* Plot each path */}
          {data.paths.map((_, pathIdx) => (
            <Line
              key={`path${pathIdx}`}
              type="monotone"
              dataKey={`path${pathIdx}`}
              stroke={`hsl(${pathIdx * 360 / data.num_paths}, 70%, 50%)`}
              strokeWidth={1}
              dot={false}
              opacity={0.3}
              isAnimationActive={false}
            />
          ))}
          
          {/* Final win rate reference line */}
          <ReferenceLine
            y={data.final_win_rate_a}
            stroke="red"
            strokeDasharray="5 5"
            strokeWidth={2}
            label={{
              value: `Final: ${(data.final_win_rate_a * 100).toFixed(1)}%`,
              position: 'right'
            }}
          />
        </LineChart>
      </ResponsiveContainer>
      
      <div className="mt-4 text-sm text-gray-600">
        <p>Convergence: {(data.final_win_rate_a * 100).toFixed(1)}% ± {(data.convergence_std * 100).toFixed(1)}%</p>
        <p>95% CI: [{(data.ci_lower * 100).toFixed(1)}%, {(data.ci_upper * 100).toFixed(1)}%]</p>
      </div>
    </div>
  );
};
```

### Usage Example
Create `frontend/src/pages/Visualization.tsx`:

```typescript
import React, { useState } from 'react';
import { MonteCarloPathsChart } from '../components/MonteCarloPathsChart';
import { api } from '../services/api';
import type { MonteCarloVisualizationResponse } from '../services/types';

export const VisualizationPage: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<MonteCarloVisualizationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const runVisualization = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.getMonteCarloVisualization({
        strategy_a: 'blocking',
        strategy_b: 'random',
        num_games: 500,
        num_paths: 100,
        seed: 12345
      });
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-8">Monte Carlo Visualization</h1>
      
      <button
        onClick={runVisualization}
        disabled={loading}
        className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded disabled:opacity-50"
      >
        {loading ? 'Generating...' : 'Run Simulation'}
      </button>
      
      {error && (
        <div className="mt-4 p-4 bg-red-100 text-red-700 rounded">
          Error: {error}
        </div>
      )}
      
      {data && <MonteCarloPathsChart data={data} />}
    </div>
  );
};
```

---

## Next Steps

### Phase 4A: API Implementation (Remaining)
- [ ] Create `/game/run` endpoint for single game simulation
- [ ] Create `/monte-carlo/compare` endpoint for strategy comparison
- [ ] Add API documentation with OpenAPI/Swagger
- [ ] Add CORS configuration for production

### Phase 4B: Frontend Implementation
- [ ] Initialize Next.js/Vite project
- [ ] Implement `MonteCarloPathsChart` component
- [ ] Add strategy selector dropdown
- [ ] Add loading states and error handling
- [ ] Add export to PNG/SVG functionality
- [ ] Style with Tailwind CSS

### Phase 5: Testing & Integration
- [ ] E2E tests with Playwright/Cypress
- [ ] API integration tests
- [ ] Performance testing (50,000 simulations)
- [ ] Cross-browser testing

### Phase 6: Documentation & Deployment
- [ ] API documentation
- [ ] User guide
- [ ] Docker compose setup
- [ ] CI/CD pipeline

---

## File Summary

**Backend Files (8 new/modified)**:
- `backend/src/aggregation/monte_carlo.py` - Added visualization data generation
- `backend/src/api/schemas/visualization.py` - NEW
- `backend/src/api/routes/visualization.py` - NEW
- `backend/src/api/routes/__init__.py` - NEW
- `backend/src/api/main.py` - NEW
- `backend/tests/unit/test_monte_carlo_visualization.py` - NEW (6 tests)
- `backend/examples/test_api.py` - NEW
- `backend/requirements.txt` - Updated (matplotlib, numpy, requests)

**Spec Files (3 modified)**:
- `specs/001-des-domino-simulation/spec.md` - Added User Story 5
- `specs/001-des-domino-simulation/data-model.md` - Added visualization entity
- `specs/001-des-domino-simulation/plan.md` - Updated structure

**Documentation (2 new)**:
- `backend/docs/monte_carlo_visualization.md` - Complete usage guide
- `MONTE_CARLO_VISUALIZATION.md` - Project-level summary

---

## Test Status

**Unit Tests**: ✅ 58/58 passing  
**Coverage**: ✅ 86%  
**API Server**: ✅ Running on port 8001  
**Health Check**: ✅ Responding  

**Performance**:
- 100 paths × 500 games = 50,000 simulations
- Estimated time: 25-30 seconds
- Memory: < 100MB

---

## Key Achievements

✅ Complete spec updates with User Story 5  
✅ Backend API endpoint functional  
✅ Visualization data generation method working  
✅ 6 new tests passing (100% coverage for new code)  
✅ FastAPI server running and responding  
✅ Comprehensive documentation created  
✅ Frontend implementation guide provided  

**Status**: Backend COMPLETE, Frontend GUIDE PROVIDED  
**Next**: Implement React frontend components
