import { useEffect, useRef, useState } from 'react'
import { get } from '../api'
import { usePoll } from '../usePoll'
import type { LedgerEntry, Verify } from '../types'
import { relativeTime } from '../format'

const SHOW = 14

/** The Proof Ledger drawn as a chain: each block holds the hash of the one before it. */
export function ChainStrip() {
  const { data: entries } = usePoll<LedgerEntry[]>(() => get('/api/ledger'))
  const { data: verify } = usePoll<Verify>(() => get('/api/ledger/verify'))
  const [picked, setPicked] = useState<number | null>(null)
  const track = useRef<HTMLOListElement>(null)

  const chain = [...(entries ?? [])].sort((a, b) => a.id - b.id).slice(-SHOW)
  const brokenAt = verify?.broken_at ?? null
  const newest = chain[chain.length - 1]?.id

  useEffect(() => {
    const el = track.current
    if (el) el.scrollTo({ left: el.scrollWidth, behavior: 'smooth' })
  }, [newest])

  if (!chain.length) return null
  const sel = chain.find((e) => e.id === picked) ?? chain[chain.length - 1]

  return (
    <section className="chain" aria-label="Proof chain">
      <div className="chain__head">
        <h3 className="chain__title">Proof chain</h3>
        <p className="chain__status">
          {brokenAt === null
            ? `${verify?.checked ?? chain.length} records sealed, every link verified`
            : `Link broken at record #${brokenAt}`}
        </p>
      </div>

      <ol className="chain__track" ref={track}>
        {chain.map((e, i) => {
          const bad = brokenAt !== null && e.id >= brokenAt
          return (
            <li key={e.id} className="chain__item" style={{ '--i': i } as React.CSSProperties}>
              {i > 0 && <span className={`chain__link${bad ? ' chain__link--bad' : ''}`} aria-hidden="true" />}
              <button
                type="button"
                className={`chain__block${bad ? ' chain__block--bad' : ''}${sel.id === e.id ? ' is-picked' : ''}`}
                aria-pressed={sel.id === e.id}
                onClick={() => setPicked(e.id)}
              >
                <span className="chain__id">#{e.id}</span>
                <span className="chain__kind">{e.kind.replace('_', ' ')}</span>
                <span className="chain__hash">{e.hash.slice(0, 8)}</span>
              </button>
            </li>
          )
        })}
      </ol>

      <div className="chain__detail" aria-live="polite">
        <p className="chain__summary">
          <strong>#{sel.id}</strong> {sel.summary}
        </p>
        <p className="chain__hashes">
          <span>seals {sel.hash.slice(0, 16)}…</span>
          <span>after {sel.prev_hash ? `${sel.prev_hash.slice(0, 16)}…` : 'genesis'}</span>
          <span>{sel.subject_id} · {relativeTime(sel.created_at)}</span>
        </p>
      </div>
    </section>
  )
}
