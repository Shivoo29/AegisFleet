/** API client. Mocks are enabled only with VITE_USE_MOCKS=true. */

import {
  summaryMock,
  approvalsMock,
  runsMock,
  ledgerMock,
  verifyMock,
  healthMock,
  disputesMock,
  disputeDetailMock,
  invoicesMock,
  inboxScamVerdict,
} from './mocks/data'

export const USE_MOCKS = import.meta.env.VITE_USE_MOCKS === 'true'

const BASE = import.meta.env.VITE_API_BASE || ''

const MOCKS: Record<string, unknown> = {
  summary: summaryMock,
  approvals: approvalsMock,
  runs: runsMock,
  ledger: ledgerMock,
  verify: verifyMock,
  health: healthMock,
  disputes: disputesMock,
  dispute_detail: disputeDetailMock,
  invoices: invoicesMock,
}

function loadMock<T>(name: string): T {
  const data = MOCKS[name]
  if (data === undefined) return [] as unknown as T
  return (Array.isArray(data) ? [...data] : { ...data }) as T
}

/** FastAPI errors are {"detail": "..."}; show the sentence, not the JSON. */
async function errorText(res: Response): Promise<string> {
  const text = await res.text()
  try {
    const d = JSON.parse(text).detail
    if (typeof d === 'string') return d
  } catch { /* not JSON */ }
  return text || res.statusText
}

export async function get<T>(path: string): Promise<T> {
  if (USE_MOCKS) {
    if (path.startsWith('/api/summary')) return loadMock<T>('summary')
    if (path.startsWith('/api/approvals')) return loadMock<T>('approvals')
    if (path.startsWith('/api/runs')) return loadMock<T>('runs')
    if (path.startsWith('/api/ledger/verify')) return loadMock<T>('verify')
    if (path.startsWith('/api/ledger')) return loadMock<T>('ledger')
    if (path.startsWith('/api/health')) return loadMock<T>('health')
    if (path.match(/^\/api\/disputes\/[^/]+$/)) return loadMock<T>('dispute_detail')
    if (path.startsWith('/api/disputes')) return loadMock<T>('disputes')
    if (path.startsWith('/api/invoices')) return loadMock<T>('invoices')
    if (path.startsWith('/api/demo/status')) return { ok: true } as T
    return [] as unknown as T
  }
  const res = await fetch(`${BASE}${path}`, { credentials: 'include' })
  if (res.status === 401) window.dispatchEvent(new Event('aegis:unauthorized'))
  if (!res.ok) throw new Error(await errorText(res))
  return res.json()
}

export async function post<T>(path: string, body: unknown): Promise<T> {
  if (USE_MOCKS) {
    if (path.includes('/approvals/') && path.endsWith('/approve')) {
      return { ok: true, status: 'approved' } as T
    }
    if (path.includes('/approvals/') && path.endsWith('/reject')) {
      return { ok: true, status: 'rejected' } as T
    }
    if (path === '/api/ledger/verify') return loadMock<T>('verify')
    if (path === '/api/inbox') return { ...inboxScamVerdict } as T
    if (path === '/api/shipments') return { ok: true, sealed: true } as T
    if (path.startsWith('/api/demo/')) {
      const name = path.replace('/api/demo/', '')
      return { ok: true, message: `Demo beat "${name}" ran on mocks` } as T
    }
    return { ok: true } as T
  }
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(body),
  })
  if (res.status === 401) window.dispatchEvent(new Event('aegis:unauthorized'))
  if (!res.ok) throw new Error(await errorText(res))
  return res.json()
}

export async function patch<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(body),
  })
  if (res.status === 401) window.dispatchEvent(new Event('aegis:unauthorized'))
  if (!res.ok) throw new Error(await errorText(res))
  return res.json()
}
