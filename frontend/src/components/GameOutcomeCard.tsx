import type { GameOutcomeSchema } from '../api/types';

interface Props {
  outcome: GameOutcomeSchema;
}

export function GameOutcomeCard({ outcome }: Props) {
  return (
    <div className="feature-card">
      <h3>Game Result</h3>
      <div className="result-grid">
        <div>
          <span className="label">Winner</span>
          <span className="value winner">{outcome.winner}</span>
        </div>
        <div>
          <span className="label">Score differential</span>
          <span className="value">{outcome.score_differential}</span>
        </div>
        <div>
          <span className="label">Turns</span>
          <span className="value">{outcome.turns}</span>
        </div>
        <div>
          <span className="label">Seed</span>
          <span className="value">{outcome.seed}</span>
        </div>
        <div>
          <span className="label">Timestamp</span>
          <span className="value" style={{ fontSize: '0.85rem' }}>{outcome.timestamp}</span>
        </div>
      </div>
    </div>
  );
}
