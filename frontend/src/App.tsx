import { useEffect, useState } from 'react'
import { AnimatePresence, MotionConfig, motion } from 'motion/react'
import { SPRING } from './components/Motion'
import { USE_MOCKS, get } from './api'
import { usePoll } from './usePoll'
import Login, { type Me } from './screens/Login'
import Tour from './components/Tour'
import './theme.css'
import Ledger from './screens/Ledger'
import Approvals from './screens/Approvals'
import Activity from './screens/Activity'
import Disputes from './screens/Disputes'
import Inbox from './screens/Inbox'
import Invoices from './screens/Invoices'
import Overview from './screens/Overview'
import Health from './screens/Health'
import Demo from './screens/Demo'

const TABS = [
  'Overview',
  'Approvals',
  'Ledger',
  'Activity',
  'Inbox',
  'Disputes',
  'Invoices',
  'Health',
  'Demo',
] as const

type Tab = (typeof TABS)[number]

export default function App() {
  const [active, setActive] = useState<Tab>('Overview')
  // undefined = checking session, null = logged out
  const [me, setMe] = useState<Me | null | undefined>(USE_MOCKS ? { user: 'dev', role: 'dev' } : undefined)

  useEffect(() => {
    if (USE_MOCKS) return
    fetch('/api/me', { credentials: 'include' })
      .then((r) => (r.ok ? r.json() : null))
      .then(setMe)
      .catch(() => setMe(null))
    const onUnauthorized = () => setMe(null)
    window.addEventListener('aegis:unauthorized', onUnauthorized)
    return () => window.removeEventListener('aegis:unauthorized', onUnauthorized)
  }, [])

  async function logout() {
    await fetch('/api/logout', { method: 'POST', credentials: 'include' }).catch(() => undefined)
    setMe(null)
  }

  if (me === undefined) return null
  if (me === null) return <Login onLogin={setMe} />

  return (
    <MotionConfig reducedMotion="user">
    <div className="app">
      <header className="header">
        <div className="header__brand">
          <div className="header__mark" aria-hidden="true">
            <svg className="header__symbol" viewBox="0 0 32 32" focusable="false">
              <path
                d="M16 3.5 26 7.3v7.3c0 6.2-3.8 11.1-10 14.1-6.2-3-10-7.9-10-14.1V7.3L16 3.5Z"
                fill="none"
                stroke="currentColor"
                strokeLinejoin="round"
                strokeWidth="1.7"
              />
              <path
                d="m10.5 15.8 3.6 3.6 7.4-7.4"
                fill="none"
                stroke="currentColor"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
              />
            </svg>
          </div>
          <div className="header__brand-copy">
            <h1 className="header__logo">AegisFleet</h1>
            <span className="header__descriptor">Seller console</span>
          </div>
        </div>

        <nav className="tabs" aria-label="Main">
          {TABS.map((t) => (
            <button
              key={t}
              type="button"
              data-tour={`tab-${t}`}
              className={active === t ? 'active' : ''}
              aria-current={active === t ? 'page' : undefined}
              onClick={() => setActive(t)}
            >
              {t}
              {active === t && <motion.span layoutId="tab-indicator" className="tabs__indicator" transition={SPRING} />}
            </button>
          ))}
        </nav>

        <div className="header__controls">
          <HeaderStatus onOpen={setActive} />
          <span className="badge">{me.role === 'judge' ? 'Judge' : me.user}</span>
          <button type="button" className="btn btn--ghost btn--sm" onClick={logout}>
            Log out
          </button>
        </div>
      </header>

      <Tour />

      <main className="main">
        <AnimatePresence mode="wait" initial={false}>
          <motion.div
            key={active}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0, transition: { duration: 0.2, ease: [0.2, 0, 0, 1] } }}
            exit={{ opacity: 0, transition: { duration: 0.1 } }}
          >
            {active === 'Overview' && <Overview />}
            {active === 'Ledger' && <Ledger />}
            {active === 'Approvals' && <Approvals />}
            {active === 'Activity' && <Activity />}
            {active === 'Disputes' && <Disputes />}
            {active === 'Inbox' && <Inbox />}
            {active === 'Invoices' && <Invoices />}
            {active === 'Health' && <Health />}
            {active === 'Demo' && <Demo />}
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
    </MotionConfig>
  )
}

type HeaderSummary = { chain_ok: boolean; pending_approvals: number; kill_switch: boolean }

/** Live header badges from /api/summary: chain integrity, kill switch, pending approvals. */
function HeaderStatus({ onOpen }: { onOpen: (t: Tab) => void }) {
  const { data, error } = usePoll(() => get<HeaderSummary>('/api/summary'))
  if (error && !data) return <span className="badge badge--amber badge--dot">Status unavailable</span>
  if (!data) return null
  const pending = data.pending_approvals
  return (
    <>
      <button type="button" className={`badge badge--dot badge--button ${data.chain_ok ? 'badge--green' : 'badge--red'}`}
        onClick={() => onOpen('Ledger')} title="Open the Proof Ledger">
        {data.chain_ok ? 'Chain intact' : 'Chain broken'}
      </button>
      {data.kill_switch && <span className="badge badge--red badge--dot">Kill switch on</span>}
      <button type="button" className={`badge badge--dot badge--button ${pending ? 'badge--amber' : 'badge--green'}`}
        onClick={() => onOpen('Approvals')} title="Open Approvals">
        {pending ? `${pending} awaiting approval` : 'No approvals waiting'}
      </button>
    </>
  )
}
