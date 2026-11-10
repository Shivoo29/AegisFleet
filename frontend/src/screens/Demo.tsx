import { useState } from 'react'
import { get, post } from '../api'

type Beat = {
  id: string
  title: string
  description: string
  path: string
}

const BEATS: Beat[] = [
  {
    id: 'sandbox_invoice',
    title: 'Real PayPal invoice',
    description: 'Issue a real $600 invoice in the PayPal sandbox. Pay it as the sandbox buyer and the signed webhook marks it paid here.',
    path: '/api/demo/sandbox_invoice',
  },
  {
    id: 'sandbox_record_payment',
    title: 'Record payment (backup)',
    description: 'If sandbox checkout fails, record the payment on the latest PayPal invoice. PayPal sends the same signed webhook.',
    path: '/api/demo/sandbox_record_payment',
  },
  {
    id: 'scam_email',
    title: 'Fake payment email',
    description: 'Inject a scam “payment received” email. Sentinel should flag it and keep the ship gate closed.',
    path: '/api/demo/scam_email',
  },
  {
    id: 'overdue',
    title: 'Overdue invoice',
    description: 'INV-0006 slips 9 days past due. Collector picks a tone and sends a capped reminder through the gateway.',
    path: '/api/demo/overdue',
  },
  {
    id: 'delivered',
    title: 'Mark delivered',
    description: 'Simulate courier delivery for INV-0007 so Defender can build a strong evidence pack.',
    path: '/api/demo/delivered',
  },
  {
    id: 'replay_injection',
    title: 'Replay injection attempt',
    description: 'An email tries to trick Sentinel into a refund. The gateway denies it and seals the attempt.',
    path: '/api/demo/replay_injection',
  },
  {
    id: 'tamper',
    title: 'Tamper with ledger',
    description: 'Edit a sealed record behind the chain\'s back. The header and Ledger point at the exact record.',
    path: '/api/demo/tamper',
  },
  {
    id: 'reset',
    title: 'Reset demo state',
    description: 'Clear demo injections and restore the baseline story for Riya’s shop.',
    path: '/api/demo/reset',
  },
]

/** A personal MCP link (signed token, 14 days) so any AI client can drive the shop through the gateway. */
const CLIENTS: { name: string; steps: (url: string) => string }[] = [
  { name: 'ChatGPT', steps: (u) => `Settings → Apps & Connectors → Advanced → turn on Developer mode → Create connector.\nURL: ${u}\nAuthentication: No authentication. Then pick the connector in a chat.` },
  { name: 'Claude.ai', steps: (u) => `Settings → Connectors → Add custom connector.\nURL: ${u}\nThen enable it from the tools menu in a chat.` },
  { name: 'Claude Code', steps: (u) => `claude mcp add --transport http aegisfleet "${u}"` },
  { name: 'Cursor / Windsurf', steps: (u) => `Add to mcp.json:\n{ "mcpServers": { "aegisfleet": { "url": "${u}" } } }` },
  { name: 'VS Code Copilot', steps: (u) => `Add to .vscode/mcp.json:\n{ "servers": { "aegisfleet": { "type": "http", "url": "${u}" } } }` },
  { name: 'Antigravity', steps: (u) => `Agent panel → … → MCP Servers → Manage MCP Servers → View raw config, add:\n{ "mcpServers": { "aegisfleet": { "serverUrl": "${u}" } } }\nSave, then refresh the server list.` },
  { name: 'Gemini CLI', steps: (u) => `Add to ~/.gemini/settings.json:\n{ "mcpServers": { "aegisfleet": { "httpUrl": "${u}" } } }` },
  { name: 'Codex CLI', steps: (u) => `Add to ~/.codex/config.toml:\n[mcp_servers.aegisfleet]\nurl = "${u}"` },
]

function ConnectAgent() {
  const [url, setUrl] = useState('')
  const [client, setClient] = useState(CLIENTS[0].name)
  const [copied, setCopied] = useState(false)
  const steps = CLIENTS.find((c) => c.name === client)!.steps(url || '<click Get my MCP link>')
  return (
    <article className="list-card connect-agent" data-tour="connect-agent">
      <h3 className="list-card__title">Connect any AI agent</h3>
      <p className="list-card__meta">
        AegisFleet is an MCP server. Connect ChatGPT, Claude, Gemini, Cursor or any MCP client and let it bill and refund on
        PayPal. It goes through the same gateway: refunds of $100 or more land in Approvals for you, and every call is sealed
        in the Ledger. Your link works for 14 days; don't share it.
      </p>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
        <button type="button" className="btn btn--secondary btn--sm"
          onClick={() => get<{ url: string }>('/api/mcp/link').then((r) => setUrl(r.url))}>
          {url ? 'New link' : 'Get my MCP link'}
        </button>
        <select className="select" style={{ width: 'auto' }} value={client} onChange={(e) => setClient(e.target.value)}>
          {CLIENTS.map((c) => <option key={c.name}>{c.name}</option>)}
        </select>
      </div>
      <pre className="connect-agent__cmd">{steps}</pre>
      <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
        <button type="button" className="btn btn--ghost btn--sm" disabled={!url}
          onClick={() => navigator.clipboard.writeText(client === 'Claude Code' ? steps : url).then(() => setCopied(true))}>
          {copied ? 'Copied' : client === 'Claude Code' ? 'Copy command' : 'Copy link'}
        </button>
        <span className="list-card__meta">
          Then ask: “Invoice a buyer $150 for a silver bangle.” After it's paid: “It arrived bent, refund it.”
        </span>
      </div>
    </article>
  )
}

export default function Demo() {
  const [busyId, setBusyId] = useState<string | null>(null)
  const [log, setLog] = useState<{ id: string; ok: boolean; message: string; link?: string }[]>([])
  const [available, setAvailable] = useState<boolean | null>(null)

  async function checkStatus() {
    try {
      await get('/api/demo/status')
      setAvailable(true)
    } catch {
      setAvailable(false)
    }
  }

  // fire once on mount via idle check button only — keep simple for mocks
  if (available === null) {
    void checkStatus()
  }

  async function run(beat: Beat) {
    setBusyId(beat.id)
    try {
      const res = await post<{ ok?: boolean; message?: string; link?: string }>(beat.path, {})
      setLog((prev) => [
        {
          id: beat.id,
          ok: res?.ok !== false,
          message: res?.message || `${beat.title} completed`,
          link: res?.link,
        },
        ...prev,
      ].slice(0, 8))
    } catch (e) {
      setLog((prev) => [
        { id: beat.id, ok: false, message: (e as Error).message || 'Failed' },
        ...prev,
      ].slice(0, 8))
    } finally {
      setBusyId(null)
    }
  }

  return (
    <div className="screen">
      <div className="screen__header">
        <div>
          <h2 className="screen__title">Demo panel</h2>
          <p className="screen__subtitle">
            One-click story beats for the video and judges. Start with Reset demo state.
          </p>
        </div>
        <span className={`badge ${available === false ? 'badge--amber' : 'badge--green'}`}>
          {available === false ? 'Mock demo mode' : 'Demo routes ready'}
        </span>
      </div>

      <div className="screen__body">
        <ConnectAgent />
        <div className="list" style={{ marginBottom: '1.25rem' }}>
          {BEATS.map((beat) => (
            <article key={beat.id} className="list-card">
              <div className="list-card__head">
                <div>
                  <h3 className="list-card__title">{beat.title}</h3>
                  <p className="list-card__meta">{beat.description}</p>
                </div>
                <button
                  type="button"
                  className="btn btn--secondary btn--sm"
                  data-tour={`beat-${beat.id}`}
                  disabled={busyId === beat.id}
                  onClick={() => run(beat)}
                >
                  {busyId === beat.id ? 'Running…' : 'Run'}
                </button>
              </div>
            </article>
          ))}
        </div>

        <h3 style={{ margin: '0 0 0.5rem', fontSize: 'var(--text-base)' }}>Last results</h3>
        {log.length === 0 && (
          <p className="list-card__meta" style={{ margin: 0 }}>
            Run a beat to see results here.
          </p>
        )}
        <ul style={{ margin: 0, paddingLeft: '1.1rem' }}>
          {log.map((entry, i) => (
            <li key={i} style={{ marginBottom: '0.35rem', fontSize: 'var(--text-sm)' }}>
              <span className={`badge ${entry.ok ? 'badge--green' : 'badge--red'}`}>
                {entry.ok ? 'ok' : 'fail'}
              </span>{' '}
              {entry.message}
              {entry.link && (
                <>
                  {' '}
                  <a href={entry.link} target="_blank" rel="noreferrer">Open the PayPal payment page</a>
                </>
              )}
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}
