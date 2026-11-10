/** Shared formatters — keep money and time consistent everywhere. */

export function money(cents: number | null | undefined, currency = 'USD'): string {
  if (cents == null) return '—'
  const value = cents / 100
  try {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency,
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(value)
  } catch {
    return `${currency} ${value.toFixed(2)}`
  }
}

export function relativeTime(iso: string): string {
  const then = new Date(iso).getTime()
  const now = Date.now()
  const sec = Math.round((now - then) / 1000)
  if (sec < 45) return 'just now'
  if (sec < 3600) return `${Math.floor(sec / 60)}m ago`
  if (sec < 86400) return `${Math.floor(sec / 3600)}h ago`
  if (sec < 604800) return `${Math.floor(sec / 86400)}d ago`
  return new Date(iso).toLocaleDateString('en-GB', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  })
}

export function agentLabel(agent: string): string {
  const map: Record<string, string> = {
    collector: 'Collector',
    sentinel: 'Sentinel',
    guardian: 'Guardian',
    defender: 'Defender',
    external: 'Outside AI agent (MCP)',
  }
  return map[agent.toLowerCase()] ?? agent
}
