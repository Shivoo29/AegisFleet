import { get } from '../api'
import { usePoll } from '../usePoll'
import type { HealthReport } from '../types'
import { StateBlock } from '../components/StateBlock'

export default function Health() {
  const { data, error, loading } = usePoll<HealthReport>(() => get('/api/health'))

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Account health</h2>
          <p className="screen__subtitle">
            Guardian’s read on holds and risk factors — what is helping or hurting settlement.
          </p>
        </div>
        {data && (
          <span
            className={`badge badge--dot ${
              data.score >= 80 ? 'badge--green' : data.score >= 50 ? 'badge--amber' : 'badge--red'
            }`}
            style={{ fontSize: '0.95rem' }}
          >
            Score {data.score}
          </span>
        )}
      </div>

      <div className="screen__body">
        {loading && !data && <StateBlock kind="loading" />}
        {error && <StateBlock kind="error" description={error.message} />}
        {!loading && !error && !data && (
          <StateBlock kind="empty" title="No health report" description="Guardian has not produced a score yet." />
        )}

        {data && (
          <>
            <h3 style={{ margin: '0 0 0.5rem', fontSize: 'var(--text-base)' }}>Factors</h3>
            <div className="list" style={{ marginBottom: '1.25rem' }}>
              {data.factors.map((f) => (
                <article key={f.name} className="list-card">
                  <div className="list-card__head">
                    <div>
                      <h3 className="list-card__title">{f.name.replace(/_/g, ' ')}</h3>
                      <p className="list-card__meta">{f.note}</p>
                    </div>
                    <span
                      className={`badge ${
                        f.impact === 'positive'
                          ? 'badge--green'
                          : f.impact === 'negative'
                            ? 'badge--red'
                            : 'badge--gray'
                      }`}
                    >
                      {f.impact}
                    </span>
                  </div>
                  <p className="list-card__meta" style={{ margin: 0 }}>
                    Value: {String(f.value)}
                  </p>
                </article>
              ))}
            </div>

            <h3 style={{ margin: '0 0 0.5rem', fontSize: 'var(--text-base)' }}>Recommendations</h3>
            <ul style={{ margin: '0 0 1.25rem', paddingLeft: '1.2rem' }}>
              {data.recommendations.map((r, i) => (
                <li key={i} style={{ marginBottom: '0.35rem', fontSize: 'var(--text-sm)' }}>
                  {r}
                </li>
              ))}
            </ul>

            {data.appeal_pack && (
              <>
                <h3 style={{ margin: '0 0 0.5rem', fontSize: 'var(--text-base)' }}>Appeal pack</h3>
                <pre
                  style={{
                    margin: 0,
                    padding: '0.85rem',
                    border: '1px solid var(--border)',
                    borderRadius: 'var(--radius)',
                    background: 'var(--bg-sunken)',
                    fontSize: 'var(--text-sm)',
                    whiteSpace: 'pre-wrap',
                  }}
                >
                  {data.appeal_pack}
                </pre>
              </>
            )}
          </>
        )}
      </div>
    </div>
  )
}
