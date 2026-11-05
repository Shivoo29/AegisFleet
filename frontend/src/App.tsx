import { useState } from 'react'
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

  return (
    <div className="app">
      <header className="header">
        <div className="header__brand">
          <div className="header__mark" aria-hidden>
            A
          </div>
          <h1 className="header__logo">AegisFleet</h1>
        </div>

        <nav className="tabs" aria-label="Main">
          {TABS.map((t) => (
            <button
              key={t}
              type="button"
              className={active === t ? 'active' : ''}
              onClick={() => setActive(t)}
            >
              {t}
            </button>
          ))}
        </nav>

        <div className="header__controls">
          <span className="badge badge--green badge--dot">Chain OK</span>
          <span className="badge badge--amber badge--dot">2 pending</span>
        </div>
      </header>

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
