import { useEffect, useState } from 'react'
import { USE_MOCKS } from './api'
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
            </button>
          ))}
        </nav>

        <div className="header__controls">
          <span className="badge badge--green badge--dot">Chain OK</span>
          <span className="badge badge--amber badge--dot">2 pending</span>
          <span className="badge">{me.role === 'judge' ? 'Judge' : me.user}</span>
          <button type="button" className="btn btn--ghost btn--sm" onClick={logout}>
            Log out
          </button>
        </div>
      </header>

      <Tour />

      <main className="main">
        {active === 'Overview' && <Overview />}
        {active === 'Ledger' && <Ledger />}
        {active === 'Approvals' && <Approvals />}
        {active === 'Activity' && <Activity />}
        {active === 'Disputes' && <Disputes />}
        {active === 'Inbox' && <Inbox />}
        {active === 'Invoices' && <Invoices />}
        {active === 'Health' && <Health />}
        {active === 'Demo' && <Demo />}
      </main>
    </div>
  )
}
