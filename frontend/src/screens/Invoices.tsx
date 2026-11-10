import { useMemo, useState } from 'react'
import { AgGridReact } from 'ag-grid-react'
import type { ColDef, ICellRendererParams } from 'ag-grid-community'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-alpine.css'

import { get, post } from '../api'
import { usePoll } from '../usePoll'
import { money, relativeTime } from '../format'
import { StateBlock } from '../components/StateBlock'

type Invoice = {
  id: string
  buyer_email: string
  amount_cents: number
  currency: string
  status: string
  days_overdue: number
  risk: string
  collector_tone: string | null
  collector_next_action: string | null
  shipped: boolean
  tracking_number: string | null
  created_at: string
  paid_at: string | null
}

function StatusCell(props: ICellRendererParams<Invoice>) {
  const s = props.value as string
  const cls =
    s === 'paid' ? 'badge--green' : s === 'overdue' ? 'badge--red' : 'badge--amber'
  return <span className={`badge ${cls}`}>{s}</span>
}

function RiskCell(props: ICellRendererParams<Invoice>) {
  const r = props.value as string
  const cls = r === 'high' ? 'badge--red' : r === 'medium' ? 'badge--amber' : 'badge--gray'
  return <span className={`badge ${cls}`}>{r}</span>
}

export default function Invoices() {
  const { data, error, loading, refetch } = usePoll<Invoice[]>(() => get('/api/invoices'))
  const [shipId, setShipId] = useState<string | null>(null)
  const [carrier, setCarrier] = useState('UPS')
  const [tracking, setTracking] = useState('')
  const [busy, setBusy] = useState(false)
  const [msg, setMsg] = useState<string | null>(null)

  const rows = data ?? []

  const colDefs = useMemo(
    () =>
      [
        { field: 'id', headerName: 'Invoice', width: 120 },
        { field: 'buyer_email', headerName: 'Buyer', flex: 1, minWidth: 180 },
        {
          field: 'amount_cents',
          headerName: 'Amount',
          width: 120,
          type: 'rightAligned',
          valueFormatter: (p: { data?: Invoice }) =>
            money(p.data?.amount_cents ?? null, p.data?.currency ?? 'USD'),
        },
        { field: 'status', headerName: 'Status', width: 110, cellRenderer: StatusCell },
        {
          field: 'days_overdue',
          headerName: 'Overdue',
          width: 100,
          valueFormatter: (p: { value?: number }) => (p.value ? `${p.value}d` : '—'),
        },
        { field: 'risk', headerName: 'Risk', width: 100, cellRenderer: RiskCell },
        {
          field: 'collector_next_action',
          headerName: 'Collector',
          width: 150,
          valueFormatter: (p: { data?: Invoice }) => {
            const d = p.data
            if (!d?.collector_next_action) return '—'
            return d.collector_tone ? `${d.collector_next_action} · ${d.collector_tone}` : d.collector_next_action
          },
        },
        {
          field: 'shipped',
          headerName: 'Shipped',
          width: 100,
          valueFormatter: (p: { value?: boolean }) => (p.value ? 'Yes' : 'No'),
        },
        {
          field: 'tracking_number',
          headerName: 'Tracking',
          width: 160,
          valueFormatter: (p: { value?: string | null }) => p.value || '—',
          cellClass: 'cell-mono',
        },
        {
          field: 'created_at',
          headerName: 'Created',
          width: 110,
          valueFormatter: (p: { value?: string }) => (p.value ? relativeTime(p.value) : ''),
        },
      ] as ColDef<Invoice>[],
    [],
  )

  const defaultColDef = useMemo(
    () => ({ sortable: true, resizable: true, suppressMovable: true }),
    [],
  )

  async function submitShipment() {
    if (!shipId || !tracking.trim()) return
    setBusy(true)
    setMsg(null)
    try {
      await post('/api/shipments', {
        invoice_id: shipId,
        carrier,
        tracking_number: tracking.trim(),
      })
      setMsg(`Tracking sealed for ${shipId}. Ship gate updated.`)
      setShipId(null)
      setTracking('')
      refetch()
    } catch (e) {
      setMsg((e as Error).message || 'Could not record shipment')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Invoices</h2>
          <p className="screen__subtitle">
            Status, risk and ship-gate. Tracking is sealed into the Proof Ledger before release.
          </p>
        </div>
      </div>

      <div className="screen__body">
        {loading && !data && <StateBlock kind="loading" />}
        {error && <StateBlock kind="error" description={error.message} />}
        {!loading && !error && rows.length === 0 && (
          <StateBlock kind="empty" title="No invoices" description="Issued invoices will appear here." />
        )}

        {rows.length > 0 && (
          <>
            <div className="ag-theme-alpine" style={{ height: 360, width: '100%', marginBottom: '1rem' }}>
              <AgGridReact<Invoice>
                rowData={rows}
                columnDefs={colDefs}
                defaultColDef={defaultColDef}
                getRowId={(p) => p.data.id}
                onRowClicked={(e) => {
                  if (e.data && !e.data.shipped) setShipId(e.data.id)
                }}
                animateRows
                suppressCellFocus
              />
            </div>

            <div
              style={{
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius)',
                padding: '1rem',
                background: 'var(--bg-elevated)',
                maxWidth: 520,
              }}
            >
              <h3 style={{ margin: '0 0 0.35rem', fontSize: 'var(--text-base)' }}>Record shipment</h3>
              <p className="list-card__meta" style={{ margin: '0 0 0.75rem' }}>
                Click an unshipped row, then add carrier + tracking. Sentinel keeps the gate closed until payment is verified.
              </p>

              <label className="label">Invoice</label>
              <input
                className="input"
                value={shipId ?? ''}
                onChange={(e) => setShipId(e.target.value || null)}
                placeholder="INV-0007"
                style={{ marginBottom: '0.6rem' }}
              />

              <label className="label">Carrier</label>
              <select
                className="select"
                value={carrier}
                onChange={(e) => setCarrier(e.target.value)}
                style={{ marginBottom: '0.6rem', width: '100%' }}
              >
                <option>UPS</option>
                <option>FedEx</option>
                <option>USPS</option>
                <option>DHL</option>
                <option>Other</option>
              </select>

              <label className="label">Tracking number</label>
              <input
                className="input"
                value={tracking}
                onChange={(e) => setTracking(e.target.value)}
                placeholder="1Z…"
                style={{ marginBottom: '0.75rem' }}
              />

              {msg && (
                <p style={{ margin: '0 0 0.6rem', fontSize: 'var(--text-sm)', color: 'var(--green)' }}>
                  {msg}
                </p>
              )}

              <button
                type="button"
                className="btn btn--primary"
                disabled={busy || !shipId || !tracking.trim()}
                onClick={submitShipment}
              >
                {busy ? 'Saving…' : 'Seal tracking & open ship gate'}
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
