import { useState } from 'react'
import { get, post } from '../api'

type Beat = {
  id: string
  title: string
  description: string
  path: string
}

const BEATS: Beat[] = [
  {
    id: 'sandbox_invoice',
    title: 'Real PayPal invoice',
    description: 'Issue a real $600 invoice in the PayPal sandbox. Pay it as the sandbox buyer and the signed webhook marks it paid here.',
    path: '/api/demo/sandbox_invoice',
  },
  {
    id: 'scam_email',
    title: 'Fake payment email',
    description: 'Inject a scam “payment received” email. Sentinel should flag it and keep the ship gate closed.',
    path: '/api/demo/scam_email',
  },
  {
    id: 'delivered',
    title: 'Mark delivered',
    description: 'Simulate courier delivery for INV-0007 so Defender can build a strong evidence pack.',
    path: '/api/demo/delivered',
  },
  {
    id: 'replay_injection',
    title: 'Replay injection attempt',
    description: 'Try to trick an agent into a money move. Gateway should hold; seller stays in control.',
    path: '/api/demo/replay_injection',
  },
  {
    id: 'tamper',
    title: 'Tamper with ledger',
    description: 'Break a hash in the Proof Ledger. Verify chain should report broken_at.',
    path: '/api/demo/tamper',
  },
  {
    id: 'reset',
    title: 'Reset demo state',
    description: 'Clear demo injections and restore the baseline story for Riya’s shop.',
    path: '/api/demo/reset',
  },
]

export default function Demo() {
  const [busyId, setBusyId] = useState<string | null>(null)
  const [log, setLog] = useState<{ id: string; ok: boolean; message: string; link?: string }[]>([])
  const [available, setAvailable] = useState<boolean | null>(null)

  async function checkStatus() {
    try {
      await get('/api/demo/status')
      setAvailable(true)
    } catch {
      setAvailable(false)
    }
  }

  // fire once on mount via idle check button only — keep simple for mocks
  if (available === null) {
    void checkStatus()
  }

  async function run(beat: Beat) {
    setBusyId(beat.id)
    try {
      const res = await post<{ ok?: boolean; message?: string; link?: string }>(beat.path, {})
      setLog((prev) => [
        {
          id: beat.id,
          ok: res?.ok !== false,
          message: res?.message || `${beat.title} completed`,
          link: res?.link,
        },
        ...prev,
      ].slice(0, 8))
    } catch (e) {
      setLog((prev) => [
        { id: beat.id, ok: false, message: (e as Error).message || 'Failed' },
        ...prev,
      ].slice(0, 8))
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Demo panel</h2>
          <p className="screen__subtitle">
            One-click story beats for the video and judges. Safe on mocks; hits live demo routes when API is real.
          </p>
        </div>
        <span className={`badge ${available === false ? 'badge--amber' : 'badge--green'}`}>
          {available === false ? 'Mock demo mode' : 'Demo routes ready'}
        </span>
      </div>

      <div className="screen__body">
        <div className="list" style={{ marginBottom: '1.25rem' }}>
          {BEATS.map((beat) => (
            <article key={beat.id} className="list-card">
              <div className="list-card__head">
                <div>
                  <h3 className="list-card__title">{beat.title}</h3>
                  <p className="list-card__meta">{beat.description}</p>
                </div>
                <button
                  type="button"
                  className="btn btn--secondary btn--sm"
                  data-tour={`beat-${beat.id}`}
                  disabled={busyId === beat.id}
                  onClick={() => run(beat)}
                >
                  {busyId === beat.id ? 'Running…' : 'Run'}
                </button>
              </div>
            </article>
          ))}
        </div>

        <h3 style={{ margin: '0 0 0.5rem', fontSize: 'var(--text-base)' }}>Last results</h3>
        {log.length === 0 && (
          <p className="list-card__meta" style={{ margin: 0 }}>
            Run a beat to see results here.
          </p>
        )}
        <ul style={{ margin: 0, paddingLeft: '1.1rem' }}>
          {log.map((entry, i) => (
            <li key={i} style={{ marginBottom: '0.35rem', fontSize: 'var(--text-sm)' }}>
              <span className={`badge ${entry.ok ? 'badge--green' : 'badge--red'}`}>
                {entry.ok ? 'ok' : 'fail'}
              </span>{' '}
              {entry.message}
              {entry.link && (
                <>
                  {' '}
                  <a href={entry.link} target="_blank" rel="noreferrer">Open the PayPal payment page</a>
                </>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
