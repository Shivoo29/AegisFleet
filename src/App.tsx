import { useState } from 'react'
import './theme.css'
import Ledger from './screens/Ledger'
import Approvals from './screens/Approvals'

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

function Placeholder({ name }: { name: string }) {
  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">{name}</h2>
          <p className="screen__subtitle">Coming in the next daily slice.</p>
        </div>
      </div>
      <div className="screen__body">
        <div className="state">
          <div className="state__icon">◌</div>
          <p className="state__title">Not built yet</p>
          <p className="state__desc">
            This screen is scheduled for a later day. Ledger and Approvals are ready today.
          </p>
        </div>
      </div>
    </div>
  )
}

export default function App() {
  const [active, setActive] = useState<Tab>('Ledger')

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

      </header>

      <main className="main">
        {active === 'Ledger' && <Ledger />}
        {active === 'Approvals' && <Approvals />}
        {active !== 'Ledger' && active !== 'Approvals' && <Placeholder name={active} />}
      </main>
    </div>
  )
}
