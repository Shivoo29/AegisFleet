import { useMemo, useState } from 'react'
import { BryntumScheduler, type BryntumSchedulerProps } from '@bryntum/scheduler-react'
import { StringHelper } from '@bryntum/scheduler'
import '@bryntum/scheduler/scheduler.css'
import '@bryntum/scheduler/stockholm-light.css'
import '@bryntum/scheduler/fontawesome/css/fontawesome.css'
import '@bryntum/scheduler/fontawesome/css/solid.css'

import { get, patch } from '../api'
import { usePoll } from '../usePoll'
import type { Approval, Run } from '../types'
import { StateBlock } from '../components/StateBlock'

// Bryntum Scheduler, driven by the agents: they put their own future actions on it (dashed), the seller
// drags them to a new time, and the runner executes each one through the gateway when it comes due.

type Dispute = { id: string; reason: string; created_at: string; due_by: string | null; amount_cents: number | null }
type Invoice = { id: string; status: string; days_overdue: number; created_at: string | null; amount_cents: number | null }
type Plan = {
  id: string; agent: string; tool: string; title: string; reason: string; subject_id: string; due_at: string
  status: 'planned' | 'running' | 'done' | 'held' | 'blocked' | 'cancelled'
  outcome: { outcome?: string; reason?: string } | null
}

const HOUR = 3600_000
const DAY = 24 * HOUR
const ROWS = [
  { id: 'sentinel', name: 'Sentinel', role: 'Scam emails', eventColor: 'teal' },
  { id: 'defender', name: 'Defender', role: 'Disputes', eventColor: 'indigo' },
  { id: 'collector', name: 'Collector', role: 'Overdue invoices', eventColor: 'orange' },
  { id: 'guardian', name: 'Guardian', role: 'Tracking and health', eventColor: 'green' },
  { id: 'external', name: 'Outside AI agents', role: 'Over MCP', eventColor: 'blue' },
  { id: 'human', name: 'You', role: 'Approvals', eventColor: 'violet' },
  { id: 'paypal', name: 'PayPal deadlines', role: 'Respond before', eventColor: 'red' },
]

const LABEL: Record<string, string> = {
  'email.received': 'Scam check', 'dispute.created': 'Evidence pack', 'dispute.updated': 'Dispute update',
  'invoice.overdue': 'Reminder', 'payment.captured': 'Payment', 'invoice.paid': 'Paid',
  'shipment.created': 'Shipped', 'delivery.confirmed': 'Delivered',
}

const PLAN_LOOK: Record<Plan['status'], { prefix: string; style: string; color?: string; word: string }> = {
  planned: { prefix: '', style: 'hollow', word: 'Planned by the agent. Drag it to move it.' },
  running: { prefix: '… ', style: 'hollow', word: 'Running now' },
  done: { prefix: '✓ ', style: 'colored', word: 'Ran through the gateway' },
  held: { prefix: '⏸ ', style: 'colored', color: 'violet', word: 'Waiting for your approval' },
  blocked: { prefix: '✕ ', style: 'colored', color: 'red', word: 'Blocked by the gateway' },
  cancelled: { prefix: '', style: 'line', color: 'gray', word: 'Cancelled' },
}

const money = (c: number | null) => (c == null ? '' : ` · $${(c / 100).toFixed(2)}`)

export default function Timeline() {
  const runs = usePoll<Run[]>(() => get('/api/runs?limit=100'))
  const approvals = usePoll<Approval[]>(() => get('/api/approvals'))
  const disputes = usePoll<Dispute[]>(() => get('/api/disputes'))
  const invoices = usePoll<Invoice[]>(() => get('/api/invoices'))
  const plans = usePoll<Plan[]>(() => get('/api/plans'))
  const [now] = useState(() => Date.now())  // fixed per visit so the view doesn't jump on every poll
  const [note, setNote] = useState('')

  const events = useMemo(() => {
    const t = Date.now()
    const out: Record<string, unknown>[] = []
    const fixed = { draggable: false, resizable: false }
    for (const r of runs.data ?? []) {
      const start = new Date(r.started_at)
      out.push({
        ...fixed, id: `run-${r.id}`, resourceId: ROWS.some((x) => x.id === r.agent) ? r.agent : 'guardian',
        name: LABEL[r.event_type] ?? r.event_type, startDate: start,
        endDate: new Date(start.getTime() + 22 * HOUR),  // ponytail: runs take seconds; a day-wide bar so the label reads
        tip: `${r.agent} handled ${r.event_type}`,
      })
    }
    for (const a of approvals.data ?? []) {
      out.push({
        ...fixed, id: `apr-${a.id}`, resourceId: 'human', name: `Waiting: ${a.tool}${money(a.amount_cents)}`,
        startDate: new Date(a.created_at), endDate: new Date(Math.max(t, new Date(a.created_at).getTime() + 22 * HOUR)),
        tip: a.summary,
      })
    }
    for (const d of disputes.data ?? []) {
      if (!d.due_by) continue
      out.push({
        ...fixed, id: `dsp-${d.id}`, resourceId: 'paypal', name: `${d.id} response due${money(d.amount_cents)}`,
        startDate: new Date(d.created_at), endDate: new Date(d.due_by),
        tip: 'PayPal decides the dispute for the buyer if the seller has not answered by the end of this bar',
      })
    }
    for (const i of invoices.data ?? []) {
      if (i.status !== 'overdue') continue
      const due = t - i.days_overdue * DAY
      out.push({
        ...fixed, id: `inv-${i.id}`, resourceId: 'collector', name: `${i.id} overdue ${i.days_overdue}d${money(i.amount_cents)}`,
        startDate: new Date(due), endDate: new Date(t), eventColor: 'red', eventStyle: 'hollow',
        tip: 'Unpaid past its due date',
      })
    }
    for (const p of plans.data ?? []) {
      const look = PLAN_LOOK[p.status]
      const start = new Date(p.due_at)
      out.push({
        id: `plan-${p.id}`, resourceId: ROWS.some((x) => x.id === p.agent) ? p.agent : 'external',
        name: `${look.prefix}${p.title}`, startDate: start, endDate: new Date(start.getTime() + 44 * HOUR),
        eventStyle: look.style, ...(look.color ? { eventColor: look.color } : {}),
        cls: p.status === 'planned' || p.status === 'running' ? 'tl-planned' : '',
        draggable: p.status === 'planned', resizable: false,
        tip: `${look.word}. ${p.reason}${p.outcome?.reason ? `. Gateway: ${p.outcome.reason}` : ''}`,
      })
    }
    return out
  }, [runs.data, approvals.data, disputes.data, invoices.data, plans.data])

  const config = useMemo<BryntumSchedulerProps>(() => ({
    startDate: new Date(now - 6 * DAY),
    endDate: new Date(now + 12 * DAY),
    visibleDate: { date: new Date(now - 3 * DAY), block: 'start' },
    viewPreset: 'weekAndDay',
    eventLayout: 'stack',
    rowHeight: 52,
    barMargin: 8,
    columns: [
      { text: 'Who', field: 'name', width: 170, renderer: ({ record }: { record: { get: (f: string) => string } }) =>
        ({ children: [{ tag: 'strong', text: record.get('name') }, { tag: 'div', className: 'tl-role', text: record.get('role') }] }) },
    ],
    features: {
      timeRanges: { showCurrentTimeLine: true },
      eventTooltip: {
        template: ({ eventRecord }: { eventRecord: { get: (f: string) => string; name: string } }) =>
          `<b>${StringHelper.encodeHtml(eventRecord.name)}</b><br>${StringHelper.encodeHtml(eventRecord.get('tip') ?? '')}`,
      },
      eventDrag: { constrainDragToResource: true },
      eventResize: false,
      eventEdit: false,
      eventDragCreate: false,
      eventMenu: false,
      scheduleMenu: false,
      cellMenu: false,
    },
  }), [now])

  async function onEventDrop({ eventRecords }: { eventRecords: { id: string | number; startDate: Date | string }[] }) {
    for (const r of eventRecords) {
      const id = String(r.id)
      if (!id.startsWith('plan-')) continue
      const when = new Date(r.startDate)
      try {
        await patch(`/api/plans/${id.slice(5)}`, { due_at: when.toISOString() })
        setNote(when.getTime() <= Date.now()
          ? 'Moved to now, so it runs within seconds: watch for ✓, or ✕ if the gateway refuses it.'
          : `Moved to ${when.toLocaleString()}. The move is sealed in the Ledger.`)
      } catch (e) {
        setNote((e as Error).message)
      }
    }
    void plans.refetch()
  }

  const loading = runs.loading && !runs.data
  const error = runs.error ?? disputes.error ?? plans.error

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Timeline</h2>
          <p className="screen__subtitle">
            The agents schedule their own next steps here. Dashed bars are planned: drag one to move it, and when it comes
            due it runs through the same gateway as everything else. The red line is now.
          </p>
        </div>
      </div>
      <div className="screen__body">
        {loading && <StateBlock kind="loading" />}
        {error && <StateBlock kind="error" description={error.message} />}
        {!loading && !error && (
          <>
            <div className="timeline-host">
              <BryntumScheduler {...config} resources={ROWS} events={events} onEventDrop={onEventDrop} />
            </div>
            <p className="tl-legend">
              <span>Dashed: planned by an agent</span><span>✓ ran through the gateway</span>
              <span>⏸ waiting for you</span><span>✕ blocked by the gateway</span>
              {note && <strong aria-live="polite">{note}</strong>}
            </p>
          </>
        )}
      </div>
    </div>
  )
}
