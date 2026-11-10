import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { AgGridReact } from 'ag-grid-react'
import type { ColDef, GetRowIdParams, ICellRendererParams, RowClassRules, RowDataUpdatedEvent } from 'ag-grid-community'
import 'ag-grid-community/styles/ag-grid.css'
import 'ag-grid-community/styles/ag-theme-alpine.css'

import { get, post } from '../api'
import { usePoll } from '../usePoll'
import type { LedgerEntry, Verify } from '../types'
import { relativeTime } from '../format'
import { StateBlock } from '../components/StateBlock'

// AG Grid Community (v32): live rows that flash on arrival, a pinned row for the broken link,
// row class rules for everything after it, a quick filter, row click for the full record, CSV export.

const KIND_BADGE: Record<string, string> = {
  event: 'badge--gray',
  decision: 'badge--green',
  agent_step: 'badge--amber',
  approval: 'badge--amber',
  note: 'badge--gray',
}

function KindCell(props: ICellRendererParams<LedgerEntry>) {
  const kind = props.value as string
  return <span className={`badge ${KIND_BADGE[kind] ?? 'badge--gray'}`}>{kind.replace('_', ' ')}</span>
}

/** Does this record still link to the one before it? Everything from the break onward is unproven. */
function LinkCell(props: ICellRendererParams<LedgerEntry> & { brokenAt: number | null }) {
  const e = props.data
  if (!e) return null
  const bad = props.brokenAt !== null && e.id >= props.brokenAt
  const label = e.prev_hash ? `#${e.id - 1} → #${e.id}` : 'genesis'
  return (
    <span className={`link-cell ${bad ? 'link-cell--bad' : ''}`} title={bad ? 'Hash does not match: this record or one before it was edited' : 'Hash matches the chain'}>
      <span aria-hidden="true">{bad ? '✕' : '✓'}</span> {label}
    </span>
  )
}

export default function Ledger() {
  const { data, error, loading } = usePoll<LedgerEntry[]>(() => get('/api/ledger'))
  const { data: liveVerify } = usePoll<Verify>(() => get('/api/ledger/verify'))
  const [verify, setVerify] = useState<Verify | null>(null)
  const [verifying, setVerifying] = useState(false)
  const [kindFilter, setKindFilter] = useState<string>('')
  const [quick, setQuick] = useState('')
  const [picked, setPicked] = useState<LedgerEntry | null>(null)
  const grid = useRef<AgGridReact<LedgerEntry>>(null)
  const seen = useRef<Set<number> | null>(null)

  const v = verify ?? liveVerify ?? null
  const brokenAt = v && !v.ok ? v.broken_at : null
  useEffect(() => setVerify(null), [liveVerify?.ok, liveVerify?.broken_at])

  const rows = useMemo(
    () => (kindFilter ? (data ?? []).filter((r) => r.kind === kindFilter) : data ?? []),
    [data, kindFilter],
  )
  const pinned = useMemo(
    () => (brokenAt === null ? [] : (data ?? []).filter((r) => r.id === brokenAt)),
    [data, brokenAt],
  )

  const colDefs = useMemo<ColDef<LedgerEntry>[]>(
    () => [
      { field: 'id', headerName: 'ID', width: 88, sort: 'desc', filter: 'agNumberColumnFilter' },
      { headerName: 'Link', width: 130, cellRenderer: LinkCell, cellRendererParams: { brokenAt }, sortable: false },
      { field: 'kind', headerName: 'Kind', width: 120, cellRenderer: KindCell, filter: 'agTextColumnFilter' },
      { field: 'subject_id', headerName: 'Subject', width: 150, cellClass: 'cell-mono', filter: 'agTextColumnFilter' },
      {
        field: 'summary', headerName: 'Summary', flex: 1, minWidth: 260, wrapText: true, autoHeight: true,
        tooltipField: 'summary', filter: 'agTextColumnFilter',
      },
      {
        field: 'created_at', headerName: 'When', width: 110,
        valueFormatter: (p) => (p.value ? relativeTime(p.value) : ''),
      },
      {
        field: 'hash', headerName: 'Hash', width: 120, cellClass: 'cell-mono cell-muted',
        valueFormatter: (p) => (p.value ? String(p.value).slice(0, 10) + '…' : ''),
      },
    ],
    [brokenAt],
  )

  const defaultColDef = useMemo<ColDef>(() => ({ sortable: true, resizable: true, suppressMovable: true, floatingFilter: false }), [])

  const rowClassRules = useMemo<RowClassRules<LedgerEntry>>(
    () => ({
      'row--broken': (p) => brokenAt !== null && p.data?.id === brokenAt,
      'row--unproven': (p) => brokenAt !== null && (p.data?.id ?? 0) > brokenAt,
    }),
    [brokenAt],
  )

  // Flash rows sealed since the last poll, so a demo beat visibly lands in the ledger.
  const onRowDataUpdated = useCallback((e: RowDataUpdatedEvent<LedgerEntry>) => {
    const ids = new Set((data ?? []).map((r) => r.id))
    if (seen.current) {
      const fresh: number[] = [...ids].filter((id) => !seen.current!.has(id))
      const nodes = fresh.map((id) => e.api.getRowNode(String(id))).filter((n) => !!n)
      if (nodes.length) e.api.flashCells({ rowNodes: nodes, flashDuration: 900, fadeDuration: 900 })
    }
    seen.current = ids
  }, [data])

  const onVerify = useCallback(async () => {
    setVerifying(true)
    try {
      setVerify(await post<Verify>('/api/ledger/verify', {}).catch(() => get<Verify>('/api/ledger/verify')))
    } catch {
      setVerify({ ok: false, checked: 0, broken_at: null })
    } finally {
      setVerifying(false)
    }
  }, [])

  const exportCsv = () =>
    grid.current?.api.exportDataAsCsv({
      fileName: `aegisfleet-proof-ledger-${new Date().toISOString().slice(0, 10)}.csv`,
      columnKeys: ['id', 'kind', 'subject_id', 'summary', 'created_at', 'hash'],
      processCellCallback: (p) => (p.column.getColId() === 'hash' ? p.node?.data?.hash ?? '' : p.value),
    })

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Proof Ledger</h2>
          <p className="screen__subtitle">
            Hash-chained, append-only record of every verified event and agent decision. Click a row to see its seal.
          </p>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap' }}>
          {v && (
            <span className={`badge ${v.ok ? 'badge--green' : 'badge--red'} badge--dot`}>
              {v.ok ? `Chain intact · ${v.checked} entries` : `Broken at #${v.broken_at}`}
            </span>
          )}
          <button className="btn btn--secondary btn--sm" onClick={onVerify} disabled={verifying}>
            {verifying ? 'Verifying…' : 'Verify chain'}
          </button>
        </div>
      </div>

      <div className="screen__body">
        <div className="grid-toolbar">
          <select className="select" style={{ width: 'auto', minWidth: 140 }} value={kindFilter} onChange={(e) => setKindFilter(e.target.value)}>
            <option value="">All kinds</option>
            <option value="event">event</option>
            <option value="decision">decision</option>
            <option value="agent_step">agent_step</option>
            <option value="approval">approval</option>
            <option value="note">note</option>
          </select>
          <input className="input" style={{ width: 240 }} placeholder="Filter by subject or text…" value={quick} onChange={(e) => setQuick(e.target.value)} />
          <button type="button" className="btn btn--ghost btn--sm grid-toolbar__end" onClick={exportCsv} disabled={!rows.length}>
            Export CSV
          </button>
        </div>

        {loading && !data && <StateBlock kind="loading" />}
        {error && <StateBlock kind="error" description={error.message} />}
        {!loading && !error && rows.length === 0 && (
          <StateBlock kind="empty" title="Ledger is empty" description="Sealed events will appear here." />
        )}

        {rows.length > 0 && (
          <div className="ag-theme-alpine aegis-grid" style={{ height: 520, width: '100%' }}>
            <AgGridReact<LedgerEntry>
              ref={grid}
              rowData={rows}
              pinnedTopRowData={pinned}
              columnDefs={colDefs}
              defaultColDef={defaultColDef}
              getRowId={(p: GetRowIdParams<LedgerEntry>) => String(p.data.id)}
              rowClassRules={rowClassRules}
              quickFilterText={quick}
              onRowDataUpdated={onRowDataUpdated}
              onRowClicked={(e) => e.data && setPicked(e.data)}
              tooltipShowDelay={300}
              animateRows
              suppressCellFocus
            />
          </div>
        )}

        {picked && (
          <aside className="seal" aria-live="polite">
            <div className="seal__head">
              <h3 className="seal__title">Record #{picked.id}</h3>
              <button type="button" className="btn btn--ghost btn--sm" onClick={() => setPicked(null)}>Close</button>
            </div>
            <p className="seal__summary">{picked.summary}</p>
            <dl className="seal__hashes">
              <dt>Seals</dt><dd>{picked.hash}</dd>
              <dt>After</dt><dd>{picked.prev_hash || 'genesis'}</dd>
              <dt>Subject</dt><dd>{picked.subject_id} · {picked.kind} · {relativeTime(picked.created_at)}</dd>
            </dl>
            <pre className="seal__payload">{JSON.stringify(picked.payload, null, 2)}</pre>
          </aside>
        )}
      </div>
    </div>
  )
}
