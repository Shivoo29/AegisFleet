import { useState } from 'react'
import { get, post } from '../api'
import { usePoll } from '../usePoll'
import type { EvidencePack } from '../types'
import { money, relativeTime } from '../format'
import { StateBlock } from '../components/StateBlock'

type DisputeRow = {
  id: string
  invoice_id: string
  reason: string
  status: string
  amount_cents: number
  currency: string
  buyer_name: string
  created_at: string
  due_by: string
}

type DisputeDetail = {
  dispute: DisputeRow
  evidence_pack: EvidencePack
  approval_id: string | null
}

export default function Disputes() {
  const { data: list, error, loading } = usePoll<DisputeRow[]>(() => get('/api/disputes'))
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [detail, setDetail] = useState<DisputeDetail | null>(null)
  const [detailLoading, setDetailLoading] = useState(false)
  const [busy, setBusy] = useState(false)
  const [doneMsg, setDoneMsg] = useState<string | null>(null)

  async function openDetail(id: string) {
    setSelectedId(id)
    setDetailLoading(true)
    setDoneMsg(null)
    try {
      const d = await get<DisputeDetail>(`/api/disputes/${id}`)
      setDetail(d)
    } catch (e) {
      console.error(e)
      setDetail(null)
    } finally {
      setDetailLoading(false)
    }
  }

  async function approveEvidence() {
    if (!detail?.approval_id) return
    setBusy(true)
    try {
      await post(`/api/approvals/${detail.approval_id}/approve`, {
        note: 'Approved from Disputes evidence view',
      })
      setDoneMsg('Evidence submission approved. Gateway will send it to PayPal.')
    } catch (e) {
      console.error(e)
      setDoneMsg('Could not approve — try again from Approvals.')
    } finally {
      setBusy(false)
    }
  }

  const rows = list ?? []

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Disputes</h2>
          <p className="screen__subtitle">
            Defender builds the evidence pack from sealed ledger proof. You approve before it goes to PayPal.
          </p>
        </div>
      </div>

      <div className="screen__body">
        {loading && !list && <StateBlock kind="loading" />}
        {error && <StateBlock kind="error" description={error.message} />}
        {!loading && !error && rows.length === 0 && (
          <StateBlock kind="empty" title="No open disputes" description="When a buyer files a claim it will show here." />
        )}

        {rows.length > 0 && (
          <div style={{ display: 'grid', gridTemplateColumns: selectedId ? '280px 1fr' : '1fr', gap: '1rem' }}>
            {/* List */}
            <div className="list">
              {rows.map((d) => (
                <button
                  key={d.id}
                  type="button"
                  className="list-card"
                  onClick={() => openDetail(d.id)}
                  style={{
                    textAlign: 'left',
                    cursor: 'pointer',
                    borderColor: selectedId === d.id ? 'var(--accent)' : undefined,
                    boxShadow: selectedId === d.id ? '0 0 0 2px var(--accent-weak)' : undefined,
                  }}
                >
                  <div className="list-card__head">
                    <div>
                      <h3 className="list-card__title">{d.id}</h3>
                      <p className="list-card__meta">
                        {d.reason.replace(/_/g, ' ')} · {relativeTime(d.created_at)}
                      </p>
                    </div>
                    <span className="money" style={{ fontSize: '0.95rem' }}>
                      {money(d.amount_cents, d.currency)}
                    </span>
                  </div>
                  <p className="list-card__meta" style={{ margin: 0 }}>
                    Buyer: {d.buyer_name} · Invoice {d.invoice_id}
                  </p>
                </button>
              ))}
            </div>

            {/* Detail / evidence pack */}
            {selectedId && (
              <div
                style={{
                  border: '1px solid var(--border)',
                  borderRadius: 'var(--radius)',
                  padding: '1.15rem',
                  background: 'var(--bg)',
                }}
              >
                {detailLoading && <StateBlock kind="loading" />}
                {!detailLoading && !detail && (
                  <StateBlock kind="error" title="Could not load evidence" />
                )}
                {detail && (
                  <>
                    <div style={{ display: 'flex', justifyContent: 'space-between', gap: '1rem', marginBottom: '1rem' }}>
                      <div>
                        <h3 style={{ margin: 0, fontSize: 'var(--text-lg)' }}>{detail.dispute.id}</h3>
                        <p className="list-card__meta" style={{ margin: '0.25rem 0 0' }}>
                          {detail.dispute.status.replace(/_/g, ' ')} · due {relativeTime(detail.dispute.due_by)}
                        </p>
                      </div>
                      <span
                        className={`badge ${
                          detail.evidence_pack.classification === 'friendly_fraud'
                            ? 'badge--amber'
                            : detail.evidence_pack.classification === 'genuine'
                              ? 'badge--red'
                              : 'badge--gray'
                        }`}
                      >
                        {detail.evidence_pack.classification.replace(/_/g, ' ')} ·{' '}
                        {Math.round(detail.evidence_pack.confidence * 100)}%
                      </span>
                    </div>

                    {/* Checklist */}
                    <h4 style={{ margin: '0 0 0.5rem', fontSize: 'var(--text-sm)', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                      Seller Protection checklist
                    </h4>
                    <ul style={{ margin: '0 0 1.1rem', padding: 0, listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                      {Object.entries(detail.evidence_pack.checklist).map(([key, ok]) => (
                        <li key={key} style={{ fontSize: 'var(--text-sm)', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <span className={`badge ${ok ? 'badge--green' : 'badge--red'}`}>
                            {ok ? '✓' : '✗'}
                          </span>
                          {key.replace(/_/g, ' ')}
                        </li>
                      ))}
                    </ul>

                    {/* Facts linked to ledger */}
                    <h4 style={{ margin: '0 0 0.5rem', fontSize: 'var(--text-sm)', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                      Facts from Proof Ledger
                    </h4>
                    <ul style={{ margin: '0 0 1.1rem', paddingLeft: '1.1rem', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                      {detail.evidence_pack.facts.map((f, i) => (
                        <li key={i} style={{ fontSize: 'var(--text-sm)', color: 'var(--text-secondary)' }}>
                          {f.claim}{' '}
                          <span className="badge badge--gray">ledger #{f.ledger_entry_id}</span>
                        </li>
                      ))}
                    </ul>

                    {/* Draft note */}
                    <h4 style={{ margin: '0 0 0.5rem', fontSize: 'var(--text-sm)', color: 'var(--muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                      Draft note to PayPal
                    </h4>
                    <p
                      style={{
                        margin: '0 0 1.15rem',
                        fontSize: 'var(--text-sm)',
                        lineHeight: 1.5,
                        color: 'var(--text)',
                        background: 'var(--card)',
                        border: '1px solid var(--border)',
                        borderRadius: 'var(--radius-sm)',
                        padding: '0.75rem 0.9rem',
                      }}
                    >
                      {detail.evidence_pack.note_to_paypal}
                    </p>

                    {doneMsg && (
                      <p style={{ margin: '0 0 0.75rem', fontSize: 'var(--text-sm)', color: 'var(--green)' }}>
                        {doneMsg}
                      </p>
                    )}

                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      <button
                        className="btn btn--primary"
                        disabled={busy || !detail.approval_id || !!doneMsg}
                        onClick={approveEvidence}
                      >
                        {busy ? 'Submitting…' : 'Approve & submit evidence'}
                      </button>
                      <button className="btn btn--ghost" onClick={() => { setSelectedId(null); setDetail(null) }}>
                        Close
                      </button>
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
