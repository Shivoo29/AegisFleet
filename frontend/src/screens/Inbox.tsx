import { useState } from 'react'
import { post } from '../api'
import type { SentinelVerdict } from '../types'
import { StateBlock } from '../components/StateBlock'

type InboxResult = {
  run_id: string
  verdict: SentinelVerdict
}

const SAMPLE_SCAM = `From: support@paypa1-support.com
Subject: Payment received — ship now

Dear Riya,

We have received payment of $600.00 USD for invoice INV-0007.
Please ship the item immediately to avoid delays.

Thank you,
PayPal Support`

export default function Inbox() {
  const [from, setFrom] = useState('support@paypa1-support.com')
  const [subject, setSubject] = useState('Payment received — ship now')
  const [body, setBody] = useState(SAMPLE_SCAM)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<InboxResult | null>(null)

  async function analyze() {
    setBusy(true)
    setError(null)
    setResult(null)
    try {
      const res = await post<InboxResult>('/api/inbox', { from, subject, body })
      setResult(res)
    } catch (e) {
      setError((e as Error).message || 'Could not analyse email')
    } finally {
      setBusy(false)
    }
  }

  function loadSample() {
    setFrom('support@paypa1-support.com')
    setSubject('Payment received — ship now')
    setBody(SAMPLE_SCAM)
    setResult(null)
    setError(null)
  }

  const v = result?.verdict

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Inbox · Sentinel</h2>
          <p className="screen__subtitle">
            Paste a payment email. Sentinel checks it against the Proof Ledger before you ship.
          </p>
        </div>
        <button type="button" className="btn btn--secondary btn--sm" onClick={loadSample}>
          Load sample scam
        </button>
      </div>

      <div className="screen__body">
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'minmax(280px, 1fr) minmax(280px, 1fr)',
            gap: '1.25rem',
            alignItems: 'start',
          }}
        >
          {/* Compose */}
          <div
            style={{
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius)',
              padding: '1.1rem',
              background: 'var(--bg-elevated)',
            }}
          >
            <label className="label" htmlFor="inbox-from">
              From
            </label>
            <input
              id="inbox-from"
              className="input"
              value={from}
              onChange={(e) => setFrom(e.target.value)}
              style={{ marginBottom: '0.75rem' }}
            />

            <label className="label" htmlFor="inbox-subject">
              Subject
            </label>
            <input
              id="inbox-subject"
              className="input"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
              style={{ marginBottom: '0.75rem' }}
            />

            <label className="label" htmlFor="inbox-body">
              Body
            </label>
            <textarea
              id="inbox-body"
              className="input"
              rows={10}
              value={body}
              onChange={(e) => setBody(e.target.value)}
              style={{ resize: 'vertical', fontFamily: 'var(--font-mono)', fontSize: 'var(--text-sm)' }}
            />

            <div style={{ marginTop: '0.9rem', display: 'flex', gap: '0.5rem' }}>
              <button
                type="button"
                className="btn btn--primary"
                disabled={busy || !body.trim()}
                onClick={analyze}
              >
                {busy ? 'Analysing…' : 'Run Sentinel'}
              </button>
            </div>
          </div>

          {/* Verdict */}
          <div
            style={{
              border: '1px solid var(--border)',
              borderRadius: 'var(--radius)',
              padding: '1.1rem',
              background: 'var(--bg-elevated)',
              minHeight: 280,
            }}
          >
            {!result && !error && !busy && (
              <StateBlock
                kind="empty"
                title="No verdict yet"
                description="Paste an email and run Sentinel. Fake payment notices are blocked before you ship."
              />
            )}
            {busy && <StateBlock kind="loading" title="Sentinel is checking…" />}
            {error && <StateBlock kind="error" description={error} />}

            {v && (
              <>
                <div style={{ display: 'flex', justifyContent: 'space-between', gap: '0.75rem', marginBottom: '0.85rem' }}>
                  <h3 style={{ margin: 0, fontSize: 'var(--text-lg)' }}>Verdict</h3>
                  <span
                    className={`badge badge--dot ${
                      v.verdict === 'scam'
                        ? 'badge--red'
                        : v.verdict === 'legit'
                          ? 'badge--green'
                          : 'badge--amber'
                    }`}
                  >
                    {v.verdict} · {Math.round(v.confidence * 100)}%
                  </span>
                </div>

                <p style={{ margin: '0 0 1rem', fontSize: 'var(--text-sm)', color: 'var(--text-secondary)', lineHeight: 1.5 }}>
                  {v.explanation}
                </p>

                {v.red_flags.length > 0 && (
                  <>
                    <h4
                      style={{
                        margin: '0 0 0.45rem',
                        fontSize: 'var(--text-sm)',
                        color: 'var(--muted)',
                        textTransform: 'uppercase',
                        letterSpacing: '0.04em',
                      }}
                    >
                      Red flags
                    </h4>
                    <ul style={{ margin: '0 0 1rem', paddingLeft: '1.15rem' }}>
                      {v.red_flags.map((flag, i) => (
                        <li key={i} style={{ fontSize: 'var(--text-sm)', marginBottom: '0.3rem', color: 'var(--text)' }}>
                          {flag}
                        </li>
                      ))}
                    </ul>
                  </>
                )}

                <p className="list-card__meta" style={{ margin: 0 }}>
                  Run {result?.run_id}
                  {v.matched_payment_entry_id != null
                    ? ` · matched ledger #${v.matched_payment_entry_id}`
                    : ' · no matching payment in ledger'}
                </p>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
