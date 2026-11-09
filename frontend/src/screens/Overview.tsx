import { AnimatePresence, motion } from 'motion/react'
import { get } from '../api'
import { usePoll } from '../usePoll'
import type { Summary, Run } from '../types'
import { money, relativeTime, agentLabel } from '../format'
import { StateBlock } from '../components/StateBlock'
import { ChainStrip } from '../components/ChainStrip'
import { Ticker, SwapText, stage, rise, row } from '../components/Motion'

const count = (n: number) => String(Math.round(n))

export default function Overview() {
  const { data: summary, error: sErr, loading: sLoad } = usePoll<Summary>(() => get('/api/summary'))
  const { data: runs, error: rErr, loading: rLoad } = usePoll<Run[]>(() => get('/api/runs'))

  const loading = (sLoad && !summary) || (rLoad && !runs)
  const error = sErr || rErr

  return (
    <div className="screen">
      <motion.section className="hero" variants={stage} initial="hidden" animate="show">
        <div className="hero__glow" aria-hidden="true" />
        <motion.h2 className="hero__title" variants={rise}>
          {summary && !summary.chain_ok
            ? 'Someone edited the record.'
            : summary?.pending_approvals
              ? `${summary.pending_approvals} decision${summary.pending_approvals > 1 ? 's' : ''} waiting on you.`
              : 'Every payment accounted for.'}
        </motion.h2>
        <motion.p className="hero__sub" variants={rise}>
          Money at risk, open work, and the latest agent runs. Updated every few seconds.
        </motion.p>

        {summary && (
          <motion.div className="metrics overview__metrics" variants={rise}>
            <Stat label="Money at risk" tone="amber">
              <Ticker value={summary.money_at_risk_cents} format={(n) => money(Math.round(n), summary.currency)} />
            </Stat>
            <Stat label="Pending approvals" tone="amber">
              <Ticker value={summary.pending_approvals} format={count} />
            </Stat>
            <Stat label="Open disputes" tone="red">
              <Ticker value={summary.open_disputes} format={count} />
            </Stat>
            <Stat label="Overdue invoices" tone="red">
              <Ticker value={summary.overdue_invoices} format={count} />
            </Stat>
            <Stat label="Health score" tone="green">
              <Ticker value={summary.health_score} format={count} />
            </Stat>
            <Stat label="Proof chain" tone={summary.chain_ok ? 'green' : 'red'}>
              <SwapText text={summary.chain_ok ? 'Intact' : 'Broken'} />
            </Stat>
            <Stat label="Kill switch" tone={summary.kill_switch ? 'red' : 'gray'}>
              <SwapText text={summary.kill_switch ? 'ON' : 'Off'} />
            </Stat>
          </motion.div>
        )}
      </motion.section>

      <div className="screen__body">
        {loading && <StateBlock kind="loading" />}
        {error && <StateBlock kind="error" description={error.message} />}

        <ChainStrip />

        <h3 className="section-title">Recent agent activity</h3>
        {!runs?.length && !loading && (
          <StateBlock kind="empty" title="No recent runs" description="Agent activity will show here." />
        )}
        {!!runs?.length && (
          <div className="list">
            <AnimatePresence initial={false}>
              {runs.slice(0, 8).map((run) => (
                <motion.article key={run.id} className="list-card" layout="position" {...row}>
                  <div className="list-card__head">
                    <div>
                      <h3 className="list-card__title">
                        <span className={`agent-dot agent-dot--${run.agent}`} aria-hidden="true" />
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
                </motion.article>
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  )
}

function Stat({
  label,
  tone,
  children,
}: {
  label: string
  tone: 'green' | 'amber' | 'red' | 'gray'
  children: React.ReactNode
}) {
  return (
    <article className={`metric metric--${tone}`}>
      <div className="metric__label">{label}</div>
      <strong className="metric__value">{children}</strong>
    </article>
  )
}
