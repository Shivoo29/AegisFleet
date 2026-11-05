import { useCallback, useMemo, useState } from 'react'
import { AgGridReact } from 'ag-grid-react'
import type { ColDef, ICellRendererParams } from 'ag-grid-community'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-alpine.css'

import { get, post } from '../api'
import { usePoll } from '../usePoll'
import type { LedgerEntry, Verify } from '../types'
import { relativeTime } from '../format'
import { StateBlock } from '../components/StateBlock'

// Using the full ag-grid-community package (v32 style).
// No ModuleRegistry needed — all Community features are included.

const KIND_BADGE: Record<string, string> = {
  event: 'badge--gray',
  decision: 'badge--green',
  agent_step: 'badge--amber',
  approval: 'badge--amber',
  note: 'badge--gray',
}

function KindCell(props: ICellRendererParams<LedgerEntry>) {
  const kind = props.value as string
  return <span className={`badge ${KIND_BADGE[kind] ?? 'badge--gray'}`}>{kind}</span>
}

export default function Ledger() {
  const { data, error, loading } = usePoll<LedgerEntry[]>(() => get('/api/ledger'))
  const [verify, setVerify] = useState<Verify | null>(null)
  const [verifying, setVerifying] = useState(false)
  const [kindFilter, setKindFilter] = useState<string>('')
  const [subjectFilter, setSubjectFilter] = useState('')

  const rows = useMemo(() => {
    let list = data ?? []
    if (kindFilter) list = list.filter((r) => r.kind === kindFilter)
    if (subjectFilter.trim()) {
      const q = subjectFilter.trim().toLowerCase()
      list = list.filter(
        (r) =>
          r.subject_id.toLowerCase().includes(q) ||
          r.summary.toLowerCase().includes(q),
      )
    }
    return list
  }, [data, kindFilter, subjectFilter])

  const colDefs = useMemo(
    () =>
      [
        {
          field: 'id',
          headerName: 'ID',
          width: 70,
          maxWidth: 80,
        },
        {
          field: 'kind',
          headerName: 'Kind',
          width: 120,
          cellRenderer: KindCell,
        },
        {
          field: 'subject_id',
          headerName: 'Subject',
          width: 140,
          cellClass: 'cell-mono',
        },
        {
          field: 'summary',
          headerName: 'Summary',
          flex: 1,
          minWidth: 280,
          wrapText: true,
          autoHeight: true,
        },
        {
          field: 'created_at',
          headerName: 'When',
          width: 110,
          valueFormatter: (p: { value?: string }) => (p.value ? relativeTime(p.value) : ''),
        },
        {
          field: 'hash',
          headerName: 'Hash',
          width: 110,
          valueFormatter: (p: { value?: string }) =>
            p.value ? String(p.value).slice(0, 10) + '…' : '',
          cellClass: 'cell-mono cell-muted',
        },
      ] as ColDef<LedgerEntry>[],
    [],
  )

  const defaultColDef = useMemo(
    () => ({
      sortable: true,
      resizable: true,
      suppressMovable: true,
    }),
    [],
  )

  const onVerify = useCallback(async () => {
    setVerifying(true)
    try {
      const result = await post<Verify>('/api/ledger/verify', {})
      // also try GET in case POST is not wired
      const v = result?.ok !== undefined ? result : await get<Verify>('/api/ledger/verify')
      setVerify(v)
    } catch {
      try {
        const v = await get<Verify>('/api/ledger/verify')
        setVerify(v)
      } catch {
        setVerify({ ok: false, checked: 0, broken_at: null })
      }
    } finally {
      setVerifying(false)
    }
  }, [])

  const getRowStyle = useCallback(
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    (params: any) => {
      if (verify && !verify.ok && verify.broken_at != null && params?.data?.id === verify.broken_at) {
        return { background: 'var(--red-bg)' }
      }
      return undefined
    },
    [verify],
  )

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Proof Ledger</h2>
          <p className="screen__subtitle">
            Hash-chained, append-only record of every verified event and agent decision.
          </p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          {verify && (
            <span className={`badge ${verify.ok ? 'badge--green' : 'badge--red'} badge--dot`}>
              {verify.ok
                ? `Chain intact · ${verify.checked} entries`
                : `Broken at #${verify.broken_at}`}
            </span>
          )}
          <button className="btn btn--secondary btn--sm" onClick={onVerify} disabled={verifying}>
            {verifying ? 'Verifying…' : 'Verify chain'}
          </button>
        </div>
      </div>

      <div className="screen__body">
        <div
          style={{
            display: 'flex',
            gap: '0.75rem',
            marginBottom: '1rem',
            flexWrap: 'wrap',
            alignItems: 'center',
          }}
        >
          <select
            className="select"
            style={{ width: 'auto', minWidth: 140 }}
            value={kindFilter}
            onChange={(e) => setKindFilter(e.target.value)}
          >
            <option value="">All kinds</option>
            <option value="event">event</option>
            <option value="decision">decision</option>
            <option value="agent_step">agent_step</option>
            <option value="approval">approval</option>
            <option value="note">note</option>
          </select>
          <input
            className="input"
            style={{ width: 220 }}
            placeholder="Filter by subject or text…"
            value={subjectFilter}
            onChange={(e) => setSubjectFilter(e.target.value)}
          />
        </div>

        {loading && !data && <StateBlock kind="loading" />}
        {error && <StateBlock kind="error" description={error.message} />}
        {!loading && !error && rows.length === 0 && (
          <StateBlock kind="empty" title="Ledger is empty" description="Sealed events will appear here." />
        )}

        {rows.length > 0 && (
          <div className="ag-theme-alpine" style={{ height: 480, width: '100%' }}>
            <AgGridReact<LedgerEntry>
              rowData={rows}
              columnDefs={colDefs}
              defaultColDef={defaultColDef}
              getRowId={(p) => String(p.data.id)}
              getRowStyle={getRowStyle}
              animateRows
              suppressCellFocus
            />
          </div>
        )}
      </div>
    </div>
  )
}
