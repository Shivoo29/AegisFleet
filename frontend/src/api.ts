/** API client. Default mocks until VITE_USE_MOCKS=false (Thursday real API). */

import {
  summaryMock,
  approvalsMock,
  runsMock,
  ledgerMock,
  verifyMock,
  healthMock,
  disputesMock,
  disputeDetailMock,
} from './mocks/data'

export const USE_MOCKS = import.meta.env.VITE_USE_MOCKS !== 'false'

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
}

function loadMock<T>(name: string): T {
  const data = MOCKS[name]
  if (data === undefined) return [] as unknown as T
  return (Array.isArray(data) ? [...data] : { ...data }) as T
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
    return [] as unknown as T
  }
  const res = await fetch(`${BASE}${path}`, { credentials: 'include' })
  if (!res.ok) throw new Error(await res.text())
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
    if (path === '/api/inbox') {
      return { run_id: 'run_19', ok: true } as T
    }
    return { ok: true } as T
  }
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}