// TypeScript interfaces matching backend Pydantic schemas exactly

// ── Strategies ────────────────────────────────────────────────────────────────

export interface StrategyInfo {
  name: string;
  description: string;
}

export interface StrategiesResponse {
  strategies: StrategyInfo[];
}

// ── Game Run ──────────────────────────────────────────────────────────────────

export interface GameRunRequest {
  strategy_a: string;
  strategy_b: string;
  seed: number;
  include_trace: boolean;
}

export interface EventSchema {
  type: string;
  timestamp: number;
  data: Record<string, unknown>;
}

export interface GameOutcomeSchema {
  winner: string;
  score_differential: number;
  turns: number;
  seed: number;
  timestamp: string;
}

export interface GameRunResponse {
  outcome: GameOutcomeSchema;
  trace: EventSchema[];
}

// ── Monte Carlo Compare ───────────────────────────────────────────────────────

export interface MonteCarloCompareRequest {
  strategy_a: string;
  strategy_b: string;
  num_runs: number;
  start_seed: number;
}

export interface MonteCarloResultSchema {
  strategy_a: string;
  strategy_b: string;
  total_runs: number;
  runs_a_wins: number;
  runs_b_wins: number;
  win_rate_a: number;
  win_rate_b: number;
  mean_score_diff_a: number;
  std_dev: number;
  ci_lower: number;
  ci_upper: number;
  execution_time_seconds: number;
}

export interface MonteCarloCompareResponse {
  result: MonteCarloResultSchema;
  per_run_outcomes: GameOutcomeSchema[];
}

// ── Visualization ─────────────────────────────────────────────────────────────

export interface VisualizationRequest {
  strategy_a: string;
  strategy_b: string;
  num_games: number;
  num_paths: number;
  seed: number;
}

export interface VisualizationResponse {
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
