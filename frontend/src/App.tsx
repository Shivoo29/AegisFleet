import { useState } from 'react'
import './theme.css'

const TABS = [
  'Header',
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

export default function App() {
  const [active, setActive] = useState<typeof TABS[number]>('Overview')
  return (
    <div className="app">
      <header className="header">
        <h1 className="logo">AegisFleet</h1>
        <nav className="tabs">
          {TABS.map((t) => (
            <button
              key={t}
              className={active === t ? 'active' : ''}
              onClick={() => setActive(t)}
            >
              {t}
            </button>
          ))}
        </nav>
      </header>
      <main className="main">
        <section className="screen">
          <h2>{active}</h2>
          <p className="placeholder">Screen not yet implemented</p>
        </section>
      </main>
    </div>
  )
}