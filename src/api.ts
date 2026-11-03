/** API client. Until Thursday we prefer mocks when VITE_USE_MOCKS=true. */

import approvals from './mocks/approvals.json'
import health from './mocks/health.json'
import ledger from './mocks/ledger.json'
import runs from './mocks/runs.json'
import summary from './mocks/summary.json'
import verify from './mocks/verify.json'

export const USE_MOCKS = import.meta.env.VITE_USE_MOCKS !== 'false' // default true until real API day

const BASE = import.meta.env.VITE_API_BASE || ''

const MOCKS = {
  approvals,
  health,
  ledger,
  runs,
  summary,
  verify,
} as const

function loadMock<T>(name: keyof typeof MOCKS): T {
  return MOCKS[name] as T
}

export async function get<T>(path: string): Promise<T> {
  if (USE_MOCKS) {
    // Map common paths to mock files
    if (path.startsWith('/api/summary')) return loadMock<T>('summary')
    if (path.startsWith('/api/approvals')) return loadMock<T>('approvals')
    if (path.startsWith('/api/runs')) return loadMock<T>('runs')
    if (path.startsWith('/api/ledger/verify')) return loadMock<T>('verify')
    if (path.startsWith('/api/ledger')) return loadMock<T>('ledger')
    if (path.startsWith('/api/health')) return loadMock<T>('health')
    // fallback empty
    return [] as unknown as T
  }
  const res = await fetch(`${BASE}${path}`, { credentials: 'include' })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function post<T>(path: string, body: unknown): Promise<T> {
  if (USE_MOCKS) {
    // Optimistic local behaviour for demo flows
    if (path.includes('/approvals/') && path.endsWith('/approve')) {
      return { ok: true, status: 'approved' } as T
    }
    if (path.includes('/approvals/') && path.endsWith('/reject')) {
      return { ok: true, status: 'rejected' } as T
    }
    if (path === '/api/ledger/verify') return loadMock<T>('verify')
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
