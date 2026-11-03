import { useEffect, useState } from 'react'

export function usePoll<T>(fn: () => Promise<T>, intervalMs = 3000) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(true)

  async function tick() {
    try {
      setData(await fn())
      setError(null)
    } catch (e) {
      setError(e as Error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    tick()
    const id = setInterval(tick, intervalMs)
    return () => clearInterval(id)
  }, [intervalMs])

  return { data, error, loading, refetch: tick }
}