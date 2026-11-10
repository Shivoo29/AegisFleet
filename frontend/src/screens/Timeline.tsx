import { useMemo } from 'react'
import { BryntumScheduler, type BryntumSchedulerProps } from '@bryntum/scheduler-react'
import '@bryntum/scheduler/scheduler.css'
import '@bryntum/scheduler/stockholm-light.css'
import '@bryntum/scheduler/fontawesome/css/fontawesome.css'
import '@bryntum/scheduler/fontawesome/css/solid.css'

import { get } from '../api'
import { usePoll } from '../usePoll'
import type { Approval, Run } from '../types'
import { StateBlock } from '../components/StateBlock'

// Bryntum Scheduler: who did what, and what's due, on one timeline.
// Rows are the four agents, the seller (approvals) and PayPal's deadlines.

type Dispute = { id: string; reason: string; created_at: string; due_by: string | null; amount_cents: number | null }
type Invoice = { id: string; status: string; days_overdue: number; created_at: string | null; amount_cents: number | null }

const HOUR = 3600_000
const DAY = 24 * HOUR
const ROWS = [
  { id: 'sentinel', name: 'Sentinel', role: 'Scam emails', eventColor: 'teal' },
  { id: 'defender', name: 'Defender', role: 'Disputes', eventColor: 'indigo' },
  { id: 'collector', name: 'Collector', role: 'Overdue invoices', eventColor: 'orange' },
  { id: 'guardian', name: 'Guardian', role: 'Tracking and health', eventColor: 'green' },
  { id: 'human', name: 'You', role: 'Approvals', eventColor: 'violet' },
  { id: 'paypal', name: 'PayPal deadlines', role: 'Respond before', eventColor: 'red' },
]

const LABEL: Record<string, string> = {
  'email.received': 'Scam check', 'dispute.created': 'Evidence pack', 'dispute.updated': 'Dispute update',
  'invoice.overdue': 'Reminder', 'payment.captured': 'Payment', 'invoice.paid': 'Paid',
  'shipment.created': 'Shipped', 'delivery.confirmed': 'Delivered',
}

const money = (c: number | null) => (c == null ? '' : ` · $${(c / 100).toFixed(2)}`)

export default function Timeline() {
  const runs = usePoll<Run[]>(() => get('/api/runs?limit=100'))
  const approvals = usePoll<Approval[]>(() => get('/api/approvals'))
  const disputes = usePoll<Dispute[]>(() => get('/api/disputes'))
  const invoices = usePoll<Invoice[]>(() => get('/api/invoices'))

  const now = Date.now()
  const events = useMemo(() => {
    const out: Record<string, unknown>[] = []
    for (const r of runs.data ?? []) {
      const start = new Date(r.started_at)
      out.push({
        id: `run-${r.id}`, resourceId: ROWS.some((x) => x.id === r.agent) ? r.agent : 'guardian',
        name: LABEL[r.event_type] ?? r.event_type, startDate: start, endDate: new Date(start.getTime() + 22 * HOUR),  // ponytail: runs take seconds; a day-wide bar so the label reads
        cls: r.status === 'error' ? 'tl-error' : '',
      })
    }
    for (const a of approvals.data ?? []) {
      out.push({
        id: `apr-${a.id}`, resourceId: 'human', name: `Waiting: ${a.tool}${money(a.amount_cents)}`,
        startDate: new Date(a.created_at), endDate: new Date(Math.max(now, new Date(a.created_at).getTime() + 22 * HOUR)),
      })
    }
    for (const d of disputes.data ?? []) {
      if (!d.due_by) continue
      out.push({
        id: `dsp-${d.id}`, resourceId: 'paypal', name: `${d.id} response due${money(d.amount_cents)}`,
        startDate: new Date(d.created_at), endDate: new Date(d.due_by),
      })
    }
    for (const i of invoices.data ?? []) {
      if (i.status !== 'overdue') continue
      const due = now - i.days_overdue * DAY
      out.push({
        id: `inv-${i.id}`, resourceId: 'collector', name: `${i.id} overdue ${i.days_overdue}d${money(i.amount_cents)}`,
        startDate: new Date(due), endDate: new Date(now), eventColor: 'red', eventStyle: 'hollow',
      })
    }
    return out
  }, [runs.data, approvals.data, disputes.data, invoices.data, now])

  const config = useMemo<BryntumSchedulerProps>(() => ({
    startDate: new Date(now - 6 * DAY),
    endDate: new Date(now + 9 * DAY),
    visibleDate: { date: new Date(now - 5 * DAY), block: 'start' },
    viewPreset: 'weekAndDay',
    eventLayout: 'stack',
    rowHeight: 52,
    barMargin: 8,
    readOnly: true,
    columns: [
      { text: 'Who', field: 'name', width: 170, renderer: ({ record }: { record: { get: (f: string) => string } }) =>
        ({ children: [{ tag: 'strong', text: record.get('name') }, { tag: 'div', className: 'tl-role', text: record.get('role') }] }) },
    ],
    features: {
      timeRanges: { showCurrentTimeLine: true },
      eventTooltip: true,
      eventMenu: false,
      scheduleMenu: false,
      cellMenu: false,
    },
  }), [now])

  const loading = runs.loading && !runs.data
  const error = runs.error ?? disputes.error

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Timeline</h2>
          <p className="screen__subtitle">
            Every agent run, every decision waiting on you, and PayPal's response deadlines on one schedule. The red line is now.
          </p>
        </div>
      </div>
      <div className="screen__body">
        {loading && <StateBlock kind="loading" />}
        {error && <StateBlock kind="error" description={error.message} />}
        {!loading && !error && (
          <div className="timeline-host">
            <BryntumScheduler {...config} resources={ROWS} events={events} />
          </div>
        )}
      </div>
    </div>
  )
}
