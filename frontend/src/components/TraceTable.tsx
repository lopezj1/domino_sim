import type { EventSchema } from '../api/types';

interface Props {
  trace: EventSchema[];
}

export function TraceTable({ trace }: Props) {
  if (trace.length === 0) return null;

  return (
    <details className="trace-details">
      <summary>Event trace ({trace.length} events)</summary>
      <div style={{ overflowX: 'auto', marginTop: '0.75rem' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
          <thead>
            <tr>
              <th style={{ textAlign: 'left', padding: '0.4rem 0.75rem', borderBottom: '1px solid var(--border)' }}>
                #
              </th>
              <th style={{ textAlign: 'left', padding: '0.4rem 0.75rem', borderBottom: '1px solid var(--border)' }}>
                Type
              </th>
              <th style={{ textAlign: 'left', padding: '0.4rem 0.75rem', borderBottom: '1px solid var(--border)' }}>
                Data
              </th>
            </tr>
          </thead>
          <tbody>
            {trace.map((event) => (
              <tr key={event.timestamp} style={{ borderBottom: '1px solid var(--border)' }}>
                <td style={{ padding: '0.3rem 0.75rem', color: 'var(--text-secondary)' }}>
                  {event.timestamp}
                </td>
                <td style={{ padding: '0.3rem 0.75rem' }}>
                  <code>{event.type}</code>
                </td>
                <td style={{ padding: '0.3rem 0.75rem', color: 'var(--text-secondary)', fontFamily: 'monospace' }}>
                  {JSON.stringify(event.data)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </details>
  );
}
