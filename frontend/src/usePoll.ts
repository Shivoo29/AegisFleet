import { useCallback, useEffect, useRef, useState } from 'react'

/** Poll `fn` every `intervalMs` (default 3s). Returns latest data, error, loading, and refetch. */
export function usePoll<T>(fn: () => Promise<T>, intervalMs = 3000) {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<Error | null>(null)
  const [loading, setLoading] = useState(true)
  const fnRef = useRef(fn)
  fnRef.current = fn

  const tick = useCallback(async () => {
    try {
      setData(await fnRef.current())
      setError(null)
    } catch (e) {
      setError(e as Error)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    void tick()
    const id = setInterval(() => void tick(), intervalMs)
    return () => clearInterval(id)
  }, [intervalMs, tick])

  return { data, error, loading, refetch: tick }
}
