export const USE_MOCKS = import.meta.env.VITE_USE_MOCKS === 'true'

const BASE = import.meta.env.VITE_API_BASE || ''

export async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { credentials: 'include' })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function post<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify(body),
  })
  if (!res.ok) throw new Error(await res.text())
  return res.json()
}