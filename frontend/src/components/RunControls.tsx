
interface Props {
  loading: boolean;
  onRunGame: () => void;
  onRunMonteCarlo: () => void;
}

export function RunControls({ loading, onRunGame, onRunMonteCarlo }: Props) {
  return (
    <div className="form-row" style={{ gap: '1rem', alignItems: 'center' }}>
      <button className="btn" onClick={onRunGame} disabled={loading}>
        {loading ? <span className="loading-spinner" /> : null}
        Run Single Game
      </button>
      <button className="btn btn-secondary" onClick={onRunMonteCarlo} disabled={loading}>
        {loading ? <span className="loading-spinner" /> : null}
        Run Monte Carlo
      </button>
    </div>
  );
}
