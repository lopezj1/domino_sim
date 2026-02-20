import type { StrategyInfo } from '../api/types';

interface Props {
  strategies: StrategyInfo[];
  strategyA: string;
  strategyB: string;
  seed: number;
  includeTrace: boolean;
  onChange: (field: string, value: string | number | boolean) => void;
}

export function StrategySelector({ strategies, strategyA, strategyB, seed, includeTrace, onChange }: Props) {
  return (
    <div className="form-row">
      <div className="form-group">
        <label htmlFor="strategy-a">Strategy A</label>
        <select
          id="strategy-a"
          value={strategyA}
          onChange={(e) => onChange('strategy_a', e.target.value)}
        >
          {strategies.map((s) => (
            <option key={s.name} value={s.name}>{s.name}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="strategy-b">Strategy B</label>
        <select
          id="strategy-b"
          value={strategyB}
          onChange={(e) => onChange('strategy_b', e.target.value)}
        >
          {strategies.map((s) => (
            <option key={s.name} value={s.name}>{s.name}</option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="seed">Seed</label>
        <input
          id="seed"
          type="number"
          value={seed}
          onChange={(e) => onChange('seed', parseInt(e.target.value, 10))}
        />
      </div>

      <div className="form-group">
        <label>
          <input
            type="checkbox"
            checked={includeTrace}
            onChange={(e) => onChange('include_trace', e.target.checked)}
          />
          {' '}Include event trace
        </label>
      </div>
    </div>
  );
}
