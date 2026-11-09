import { useEffect, useLayoutEffect, useRef, useState } from 'react'

/**
 * First-visit guide. Points at the next thing to click without ever covering the page:
 * the layer ignores pointer events, only the small card is clickable.
 * Clicking the highlighted target moves on; clicking anything else pauses the guide.
 */
type Step = { target: string; title: string; body: string }

const STEPS: Step[] = [
  { target: 'tab-Demo', title: 'Start in Demo',
    body: 'This panel drives the story. Open it to load a seller’s day.' },
  { target: 'beat-reset', title: 'Load the scenario',
    body: 'Reset rebuilds Riya’s jewellery shop: a $600 order paid, shipped, delivered — then a buyer claims it never arrived.' },
  { target: 'beat-scam_email', title: 'Send a fake payment email',
    body: 'A lookalike “you got paid” email arrives. Sentinel checks the ledger for a real payment and flags it.' },
  { target: 'tab-Approvals', title: 'Review the dispute response',
    body: 'Defender drafted evidence for the dispute. Nothing reaches PayPal until a person approves it.' },
  { target: 'tab-Ledger', title: 'Check the proof',
    body: 'Every step is sealed in a hash chain. Run Tamper in Demo, then verify here to see the break.' },
]

const DONE_KEY = 'aegis.tour.done'
const readDone = () => { try { return localStorage.getItem(DONE_KEY) === '1' } catch { return false } }
const writeDone = () => { try { localStorage.setItem(DONE_KEY, '1') } catch { /* private mode: guide shows again */ } }

const find = (t: string) => document.querySelector<HTMLElement>(`[data-tour="${t}"]`)

export default function Tour() {
  const [step, setStep] = useState(0)
  const [state, setState] = useState<'on' | 'paused' | 'done'>(readDone() ? 'done' : 'on')
  const [rect, setRect] = useState<DOMRect | null>(null)
  const cardRef = useRef<HTMLDivElement>(null)
  const current = STEPS[step]

  function finish() { writeDone(); setState('done') }

  // Track the target: it may mount later (Demo screen) or move (scroll, resize).
  useLayoutEffect(() => {
    if (state !== 'on') return
    let raf = 0
    let scrolled = false
    const tick = () => {
      const el = find(current.target)
      if (el && !scrolled) { el.scrollIntoView({ block: 'nearest', inline: 'nearest' }); scrolled = true }
      const r = el?.getBoundingClientRect() ?? null
      setRect((prev) => (r && prev && r.top === prev.top && r.left === prev.left && r.width === prev.width) ? prev : r)
      raf = requestAnimationFrame(tick)
    }
    tick()
    return () => cancelAnimationFrame(raf)
  }, [state, current])

  // Never block: listen in capture phase, let every click through.
  useEffect(() => {
    if (state !== 'on') return
    const onClick = (e: MouseEvent) => {
      const t = e.target as Node
      if (cardRef.current?.contains(t)) return
      if (find(current.target)?.contains(t)) {
        if (step === STEPS.length - 1) finish()
        else setStep(step + 1)
      } else {
        setState('paused')
      }
    }
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setState('paused') }
    document.addEventListener('click', onClick, true)
    document.addEventListener('keydown', onKey)
    return () => { document.removeEventListener('click', onClick, true); document.removeEventListener('keydown', onKey) }
  }, [state, step, current])

  if (state === 'done') return null

  if (state === 'paused') {
    return (
      <div className="tour-resume" role="region" aria-label="Guide">
        <button type="button" className="tour-resume__btn" onClick={() => setState('on')}>
          Resume guide · step {step + 1} of {STEPS.length}
        </button>
        <button type="button" className="tour-resume__close" aria-label="Close guide" onClick={finish}>×</button>
      </div>
    )
  }

  if (!rect) return null

  // Card below the target if there is room, otherwise above; clamped to the viewport.
  const vw = Math.min(window.visualViewport?.width ?? Infinity, document.documentElement.clientWidth)
  const vh = document.documentElement.clientHeight
  const W = Math.min(300, vw - 24)
  const below = rect.bottom + 180 < vh
  const left = Math.max(12, Math.min(rect.left + rect.width / 2 - W / 2, vw - W - 12))
  const arrowX = Math.max(16, Math.min(rect.left + rect.width / 2 - left, W - 16))

  return (
    <div className="tour" aria-live="polite">
      <div className="tour__ring" style={{ top: rect.top - 4, left: rect.left - 4, width: rect.width + 8, height: rect.height + 8 }} />
      <div
        ref={cardRef}
        className={`tour__card ${below ? 'tour__card--below' : 'tour__card--above'}`}
        role="dialog"
        aria-label={current.title}
        style={{ width: W, left, ...(below ? { top: rect.bottom + 12 } : { bottom: vh - rect.top + 12 }),
          ['--arrow-x' as string]: `${arrowX}px` }}
      >
        <p className="tour__count">Step {step + 1} of {STEPS.length}</p>
        <h2 className="tour__title">{current.title}</h2>
        <p className="tour__body">{current.body}</p>
        <div className="tour__actions">
          <button type="button" className="tour__link" onClick={finish}>Skip guide</button>
          <span className="tour__hint">Click the highlighted button</span>
        </div>
      </div>
    </div>
  )
}
