import type { MonteCarloResultSchema } from '../api/types';

interface Props {
  result: MonteCarloResultSchema;
}

function pct(n: number) {
  return (n * 100).toFixed(1) + '%';
}

export function MonteCarloResultCard({ result }: Props) {
  return (
    <div className="feature-card">
      <h3>Monte Carlo Results</h3>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
        {result.total_runs} runs · {result.execution_time_seconds.toFixed(2)}s
      </p>
      <div className="result-grid">
        <div>
          <span className="label">{result.strategy_a} win rate</span>
          <span className="value winner">{pct(result.win_rate_a)}</span>
        </div>
        <div>
          <span className="label">{result.strategy_b} win rate</span>
          <span className="value">{pct(result.win_rate_b)}</span>
        </div>
        <div>
          <span className="label">Mean score diff</span>
          <span className="value">{result.mean_score_diff_a.toFixed(1)}</span>
        </div>
        <div>
          <span className="label">Std dev</span>
          <span className="value">{result.std_dev.toFixed(1)}</span>
        </div>
        <div>
          <span className="label">95% CI (score diff)</span>
          <span className="value">
            [{result.ci_lower.toFixed(1)}, {result.ci_upper.toFixed(1)}]
          </span>
        </div>
        <div>
          <span className="label">Wins A / B</span>
          <span className="value">{result.runs_a_wins} / {result.runs_b_wins}</span>
        </div>
      </div>
    </div>
  );
}
