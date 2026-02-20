
interface Props {
  numRuns: number;
  startSeed: number;
  onChange: (field: string, value: number) => void;
}

export function MonteCarloConfig({ numRuns, startSeed, onChange }: Props) {
  return (
    <div className="form-row">
      <div className="form-group">
        <label htmlFor="num-runs">Number of runs: <strong>{numRuns}</strong></label>
        <input
          id="num-runs"
          type="range"
          min={10}
          max={1000}
          step={10}
          value={numRuns}
          onChange={(e) => onChange('num_runs', parseInt(e.target.value, 10))}
        />
        <input
          type="number"
          min={10}
          max={100000}
          value={numRuns}
          onChange={(e) => onChange('num_runs', parseInt(e.target.value, 10))}
          style={{ width: '80px', marginLeft: '0.5rem' }}
        />
      </div>

      <div className="form-group">
        <label htmlFor="start-seed">Start seed</label>
        <input
          id="start-seed"
          type="number"
          value={startSeed}
          onChange={(e) => onChange('start_seed', parseInt(e.target.value, 10))}
        />
      </div>
    </div>
  );
}
