import { useState } from 'react'
import { get, post } from '../api'
import { usePoll } from '../usePoll'
import type { Approval } from '../types'
import { money, relativeTime, agentLabel } from '../format'
import { StateBlock } from '../components/StateBlock'

export default function Approvals() {
  const { data, error, loading, refetch } = usePoll<Approval[]>(() => get('/api/approvals'))
  const [busyId, setBusyId] = useState<string | null>(null)
  const [note, setNote] = useState<Record<string, string>>({})
  const [localStatus, setLocalStatus] = useState<Record<string, 'approved' | 'rejected'>>({})

  const items = (data ?? []).filter((a) => a.status === 'pending' && !localStatus[a.id])

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
        {error && <StateBlock kind="error" description={error.message} />}
        {!loading && !error && items.length === 0 && (
          <StateBlock
            kind="empty"
            title="All clear"
            description="No pending approvals. Agents are waiting for the next event."
          />
        )}

        {items.length > 0 && (
          <div className="list">
            {items.map((a) => (
              <article key={a.id} className="list-card">
                <div className="list-card__head">
                  <div>
                    <h3 className="list-card__title">{a.summary}</h3>
                    <p className="list-card__meta">
                      {agentLabel(a.agent)} · {a.tool} · {relativeTime(a.created_at)}
                    </p>
                  </div>
                  {a.amount_cents != null && (
                    <span className="money" style={{ fontSize: '1.05rem' }}>
                      {money(a.amount_cents, a.currency ?? 'USD')}
                    </span>
                  )}
                </div>

                <p className="list-card__body">{a.reason}</p>

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
                    className="btn btn--primary btn--sm"
                    disabled={busyId === a.id}
                    onClick={() => act(a.id, 'approve')}
                  >
                    Approve
                  </button>
                  <button
                    className="btn btn--secondary btn--sm"
                    disabled={busyId === a.id}
                    onClick={() => act(a.id, 'reject')}
                  >
                    Reject
                  </button>
                </div>
              </article>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
