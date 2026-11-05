import { useState } from 'react'
import { get } from '../api'
import { usePoll } from '../usePoll'
import type { Run } from '../types'
import { relativeTime, agentLabel } from '../format'
import { StateBlock } from '../components/StateBlock'

const STEP_LABEL: Record<string, string> = {
  llm: 'LLM',
  tool: 'Tool',
  note: 'Note',
}

export default function Activity() {
  const { data, error, loading } = usePoll<Run[]>(() => get('/api/runs'))
  const [openId, setOpenId] = useState<string | null>(null)

  const runs = data ?? []

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Agent activity</h2>
          <p className="screen__subtitle">
            Every agent run, expandable into LLM, tool and decision steps.
          </p>
        </div>
        {runs.length > 0 && (
          <span className="badge badge--gray">{runs.length} recent</span>
        )}
      </div>

      <div className="screen__body">
        {loading && !data && <StateBlock kind="loading" />}
        {error && <StateBlock kind="error" description={error.message} />}
        {!loading && !error && runs.length === 0 && (
          <StateBlock
            kind="empty"
            title="No activity yet"
            description="When agents run, their steps will appear here."
          />
        )}

        {runs.length > 0 && (
          <div className="list">
            {runs.map((run) => {
              const expanded = openId === run.id
              return (
                <article key={run.id} className="list-card">
                  <button
                    type="button"
                    onClick={() => setOpenId(expanded ? null : run.id)}
                    style={{
                      all: 'unset',
                      cursor: 'pointer',
                      display: 'block',
                      width: '100%',
                    }}
                  >
                    <div className="list-card__head">
                      <div>
                        <h3 className="list-card__title">
                          {agentLabel(run.agent)} · {run.event_type}
                        </h3>
                        <p className="list-card__meta">
                          {run.id} · {relativeTime(run.started_at)} · {run.status}
                        </p>
                      </div>
                      <span
                        className={`badge ${
                          run.status === 'done' ? 'badge--green' : 'badge--amber'
                        }`}
                      >
                        {run.status}
                      </span>
                    </div>
                  </button>

                  {expanded && (
                    <div style={{ marginTop: '0.75rem' }}>
                      <ol
                        style={{
                          margin: 0,
                          paddingLeft: '1.15rem',
                          display: 'flex',
                          flexDirection: 'column',
                          gap: '0.45rem',
                        }}
                      >
                        {run.steps.map((step, i) => (
                          <li
                            key={i}
                            style={{
                              fontSize: 'var(--text-sm)',
                              color: 'var(--text-secondary)',
                              lineHeight: 1.45,
                            }}
                          >
                            <span
                              className="badge badge--gray"
                              style={{ marginRight: '0.4rem', verticalAlign: 'middle' }}
                            >
                              {STEP_LABEL[step.kind] ?? step.kind}
                            </span>
                            {step.summary}
                          </li>
                        ))}
                      </ol>
                    </div>
                  )}
                </article>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
