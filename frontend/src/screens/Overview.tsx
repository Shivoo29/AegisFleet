import { get } from '../api'
import { usePoll } from '../usePoll'
import type { Summary, Run } from '../types'
import { money, relativeTime, agentLabel } from '../format'
import { StateBlock } from '../components/StateBlock'
import { ChainStrip } from '../components/ChainStrip'

export default function Overview() {
  const { data: summary, error: sErr, loading: sLoad } = usePoll<Summary>(() => get('/api/summary'))
  const { data: runs, error: rErr, loading: rLoad } = usePoll<Run[]>(() => get('/api/runs'))

  const loading = (sLoad && !summary) || (rLoad && !runs)
  const error = sErr || rErr

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Overview</h2>
          <p className="screen__subtitle">
            Money at risk, open work, and the latest agent runs — updated every few seconds.
          </p>
        </div>
      </div>

      <div className="screen__body">
        {loading && <StateBlock kind="loading" />}
        {error && <StateBlock kind="error" description={error.message} />}

        {summary && (
          <div className="metrics overview__metrics">
            <Stat
              label="Money at risk"
              value={money(summary.money_at_risk_cents, summary.currency)}
              tone="amber"
            />
            <Stat label="Pending approvals" value={String(summary.pending_approvals)} tone="amber" />
            <Stat label="Open disputes" value={String(summary.open_disputes)} tone="red" />
            <Stat label="Overdue invoices" value={String(summary.overdue_invoices)} tone="red" />
            <Stat label="Health score" value={String(summary.health_score)} tone="green" />
            <Stat
              label="Proof chain"
              value={summary.chain_ok ? 'Intact' : 'Broken'}
              tone={summary.chain_ok ? 'green' : 'red'}
            />
            <Stat
              label="Kill switch"
              value={summary.kill_switch ? 'ON' : 'Off'}
              tone={summary.kill_switch ? 'red' : 'gray'}
            />
          </div>
        )}

        <ChainStrip />

        <h3 className="section-title">Recent agent activity</h3>
        {!runs?.length && !loading && (
          <StateBlock kind="empty" title="No recent runs" description="Agent activity will show here." />
        )}
        {!!runs?.length && (
          <div className="list">
            {runs.slice(0, 8).map((run) => (
              <article key={run.id} className="list-card">
                <div className="list-card__head">
                  <div>
                    <h3 className="list-card__title">
                      {agentLabel(run.agent)} · {run.event_type}
                    </h3>
                    <p className="list-card__meta">
                      {run.id} · {relativeTime(run.started_at)} · {run.steps.length} steps
                    </p>
                  </div>
                  <span className={`badge ${run.status === 'done' ? 'badge--green' : 'badge--amber'}`}>
                    {run.status}
                  </span>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

function Stat({
  label,
  value,
  tone,
}: {
  label: string
  value: string
  tone: 'green' | 'amber' | 'red' | 'gray'
}) {
  return (
    <article className={`metric metric--${tone}`}>
      <div className="metric__label">{label}</div>
      <strong className="metric__value">{value}</strong>
    </article>
  )
}
