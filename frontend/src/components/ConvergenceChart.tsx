import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import type { VisualizationResponse } from '../api/types';

interface Props {
  data: VisualizationResponse;
}

const MAX_CHART_POINTS = 100;

function decimate(arr: number[], maxPoints: number): number[] {
  if (arr.length <= maxPoints) return arr;
  const step = Math.ceil(arr.length / maxPoints);
  return arr.filter((_, i) => i % step === 0);
}

export function ConvergenceChart({ data }: Props) {
  const gameNumbers = decimate(data.game_numbers, MAX_CHART_POINTS);
  const step = Math.ceil(data.game_numbers.length / MAX_CHART_POINTS);

  // Build chart data: one row per decimated game index
  const chartData = gameNumbers.map((gn, i) => {
    const srcIdx = i * step;
    const row: Record<string, number> = { game: gn };
    data.paths.forEach((path, pi) => {
      row[`path${pi}`] = path[srcIdx] ?? path[path.length - 1];
    });
    return row;
  });

  const pathKeys = data.paths.map((_, i) => `path${i}`);

  return (
    <div className="chart-container">
      <h3 style={{ marginBottom: '1rem' }}>
        Convergence: {data.strategy_a} vs {data.strategy_b}
      </h3>
      <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem', fontSize: '0.9rem' }}>
        {data.num_paths} paths · {data.total_games} games each · final win rate A:{' '}
        <strong>{(data.final_win_rate_a * 100).toFixed(1)}%</strong>
      </p>
      <ResponsiveContainer width="100%" height={340}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis
            dataKey="game"
            label={{ value: 'Game number', position: 'insideBottom', offset: -5 }}
            tick={{ fontSize: 12 }}
          />
          <YAxis
            domain={[0, 1]}
            tickFormatter={(v) => `${(v * 100).toFixed(0)}%`}
            label={{ value: `Win rate (${data.strategy_a})`, angle: -90, position: 'insideLeft', offset: 10 }}
            tick={{ fontSize: 12 }}
          />
          <Tooltip
            formatter={(v: number) => `${(v * 100).toFixed(1)}%`}
            labelFormatter={(l) => `Game ${l}`}
          />
          <Legend verticalAlign="top" />
          {pathKeys.map((key, i) => (
            <Line
              key={key}
              type="monotone"
              dataKey={key}
              stroke={`hsl(${(i * 137) % 360}, 60%, 55%)`}
              strokeWidth={1}
              dot={false}
              strokeOpacity={0.4}
              legendType="none"
              name={undefined}
            />
          ))}
          <ReferenceLine
            y={data.final_win_rate_a}
            stroke="#ef4444"
            strokeDasharray="6 3"
            strokeWidth={2}
            label={{
              value: `${(data.final_win_rate_a * 100).toFixed(1)}%`,
              fill: '#ef4444',
              fontSize: 12,
              position: 'right',
            }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
