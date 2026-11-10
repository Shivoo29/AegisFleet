import { useState } from 'react'
import { get, post } from '../api'
import { usePoll } from '../usePoll'
import type { Approval } from '../types'
import { money, relativeTime, agentLabel } from '../format'
import { StateBlock } from '../components/StateBlock'
import { AnimatePresence, motion } from 'motion/react'
import { row } from '../components/Motion'

function asApprovalList(data: unknown): Approval[] {
  if (Array.isArray(data)) return data as Approval[]
  if (data && typeof data === 'object' && Array.isArray((data as { items?: unknown }).items)) {
    return (data as { items: Approval[] }).items
  }
  return []
}

export default function Approvals() {
  const { data, error, loading, refetch } = usePoll<unknown>(() => get('/api/approvals'))
  const [busyId, setBusyId] = useState<string | null>(null)
  const [note, setNote] = useState<Record<string, string>>({})
  const [localStatus, setLocalStatus] = useState<Record<string, 'approved' | 'rejected'>>({})

  const items = asApprovalList(data).filter(
    (a) => a && a.status === 'pending' && !localStatus[a.id],
  )

  async function act(id: string, action: 'approve' | 'reject') {
    setBusyId(id)
    try {
      await post(`/api/approvals/${id}/${action}`, { note: note[id] ?? '' })
      setLocalStatus((s) => ({ ...s, [id]: action === 'approve' ? 'approved' : 'rejected' }))
      refetch()
    } catch (e) {
      console.error(e)
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Approvals</h2>
          <p className="screen__subtitle">
            Agents can only move money after you approve. Review each request carefully.
          </p>
        </div>
        {items.length > 0 && (
          <span className="badge badge--amber badge--dot">{items.length} pending</span>
        )}
      </div>

      <div className="screen__body">
        {loading && !data && <StateBlock kind="loading" />}
        {error && (
          <StateBlock
            kind="error"
            description={error instanceof Error ? error.message : 'Request failed'}
          />
        )}
        {!loading && !error && items.length === 0 && (
          <StateBlock
            kind="empty"
            title="All clear"
            description="No pending approvals. Agents are waiting for the next event."
          />
        )}

        {items.length > 0 && (
          <div className="list">
            <AnimatePresence initial={false}>
            {items.map((a) => {
              const summary = String(a.summary ?? '')
              const reason = String(a.reason ?? '')
              const tool = String(a.tool ?? '')
              const agent = String(a.agent ?? '')
              const created = String(a.created_at ?? '')
              const amountLabel =
                a.amount_cents != null ? money(a.amount_cents, a.currency ?? 'USD') : null

              return (
                <motion.article key={String(a.id)} className="list-card" layout="position" {...row}>
                  <div className="list-card__head">
                    <div>
                      <h3 className="list-card__title">{summary}</h3>
                      <p className="list-card__meta">
                        {agentLabel(agent)} · {tool}
                        {created ? ` · ${relativeTime(created)}` : ''}
                      </p>
                    </div>
                    {amountLabel != null && (
                      <span className="money" style={{ fontSize: '1.05rem' }}>
                        {amountLabel}
                      </span>
                    )}
                  </div>

                  {reason && reason !== summary ? <p className="list-card__body">{reason}</p> : null}

                  <textarea
                    className="textarea"
                    placeholder="Optional note (visible in the ledger)"
                    value={note[a.id] ?? ''}
                    onChange={(e) => setNote((n) => ({ ...n, [a.id]: e.target.value }))}
                    rows={2}
                    style={{ marginBottom: '0.75rem' }}
                  />

                  <div className="list-card__actions">
                    <button
                      type="button"
                      className="btn btn--primary btn--sm"
                      disabled={busyId === a.id}
                      onClick={() => act(a.id, 'approve')}
                    >
                      Approve
                    </button>
                    <button
                      type="button"
                      className="btn btn--secondary btn--sm"
                      disabled={busyId === a.id}
                      onClick={() => act(a.id, 'reject')}
                    >
                      Reject
                    </button>
                  </div>
                </motion.article>
              )
            })}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  )
}