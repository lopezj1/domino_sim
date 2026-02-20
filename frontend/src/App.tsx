import { useState, useEffect } from 'react';
import './styles/App.css';

import { getStrategies, runGame, compareStrategies, getVisualizationPaths } from './api/client';
import type {
  StrategyInfo,
  GameRunResponse,
  MonteCarloCompareResponse,
  VisualizationResponse,
} from './api/types';

import { StrategySelector } from './components/StrategySelector';
import { MonteCarloConfig } from './components/MonteCarloConfig';
import { RunControls } from './components/RunControls';
import { GameOutcomeCard } from './components/GameOutcomeCard';
import { MonteCarloResultCard } from './components/MonteCarloResultCard';
import { TraceTable } from './components/TraceTable';
import { ConvergenceChart } from './components/ConvergenceChart';

function App() {
  const [strategies, setStrategies] = useState<StrategyInfo[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Game config
  const [strategyA, setStrategyA] = useState('greedy');
  const [strategyB, setStrategyB] = useState('random');
  const [seed, setSeed] = useState(42);
  const [includeTrace, setIncludeTrace] = useState(false);

  // Monte Carlo config
  const [numRuns, setNumRuns] = useState(100);
  const [startSeed, setStartSeed] = useState(1000);

  // Results
  const [gameResult, setGameResult] = useState<GameRunResponse | null>(null);
  const [mcResult, setMcResult] = useState<MonteCarloCompareResponse | null>(null);
  const [vizResult, setVizResult] = useState<VisualizationResponse | null>(null);

  useEffect(() => {
    getStrategies()
      .then((res) => setStrategies(res.data.strategies))
      .catch(() => setError('Failed to load strategies from backend'));
  }, []);

  function handleConfigChange(field: string, value: string | number | boolean) {
    if (field === 'strategy_a') setStrategyA(value as string);
    else if (field === 'strategy_b') setStrategyB(value as string);
    else if (field === 'seed') setSeed(value as number);
    else if (field === 'include_trace') setIncludeTrace(value as boolean);
  }

  function handleMcChange(field: string, value: number) {
    if (field === 'num_runs') setNumRuns(value);
    else if (field === 'start_seed') setStartSeed(value);
  }

  async function handleRunGame() {
    setLoading(true);
    setError(null);
    setGameResult(null);
    setMcResult(null);
    setVizResult(null);
    try {
      const res = await runGame({ strategy_a: strategyA, strategy_b: strategyB, seed, include_trace: includeTrace });
      setGameResult(res.data);
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setError(msg ?? 'Error running game');
    } finally {
      setLoading(false);
    }
  }

  async function handleRunMonteCarlo() {
    setLoading(true);
    setError(null);
    setGameResult(null);
    setMcResult(null);
    setVizResult(null);
    try {
      const [mcRes, vizRes] = await Promise.all([
        compareStrategies({ strategy_a: strategyA, strategy_b: strategyB, num_runs: numRuns, start_seed: startSeed }),
        getVisualizationPaths({
          strategy_a: strategyA,
          strategy_b: strategyB,
          num_games: Math.min(numRuns, 500),
          num_paths: 10,
          seed: startSeed,
        }),
      ]);
      setMcResult(mcRes.data);
      setVizResult(vizRes.data);
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setError(msg ?? 'Error running Monte Carlo');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Domino Simulation</h1>
        <p className="subtitle">Monte Carlo Strategy Analysis with Visualization</p>
      </header>

      <main className="main">
        {error && (
          <div className="error-banner">
            <strong>Error:</strong> {error}
            <button onClick={() => setError(null)} style={{ marginLeft: '1rem', cursor: 'pointer' }}>✕</button>
          </div>
        )}

        <div className="status-card">
          <h2>Configure Simulation</h2>

          {strategies.length > 0 ? (
            <StrategySelector
              strategies={strategies}
              strategyA={strategyA}
              strategyB={strategyB}
              seed={seed}
              includeTrace={includeTrace}
              onChange={handleConfigChange}
            />
          ) : (
            <p style={{ color: 'var(--text-secondary)' }}>Loading strategies…</p>
          )}

          <RunControls
            loading={loading}
            onRunGame={handleRunGame}
            onRunMonteCarlo={handleRunMonteCarlo}
          />
        </div>

        <div className="status-card">
          <h2>Monte Carlo Options</h2>
          <MonteCarloConfig numRuns={numRuns} startSeed={startSeed} onChange={handleMcChange} />
        </div>

        {gameResult && (
          <div className="features" style={{ gridTemplateColumns: '1fr' }}>
            <GameOutcomeCard outcome={gameResult.outcome} />
            <TraceTable trace={gameResult.trace} />
          </div>
        )}

        {mcResult && (
          <div className="features" style={{ gridTemplateColumns: '1fr' }}>
            <MonteCarloResultCard result={mcResult.result} />
          </div>
        )}

        {vizResult && (
          <ConvergenceChart data={vizResult} />
        )}
      </main>

      <footer className="footer">
        <p>Domino Simulation — FastAPI + React + TypeScript</p>
      </footer>
    </div>
  );
}

export default App;
