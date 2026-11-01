/** TS copies of backend contract models (frozen). */

export type Summary = {
  money_at_risk_cents: number
  currency: string
  pending_approvals: number
  open_disputes: number
  overdue_invoices: number
  health_score: number
  kill_switch: boolean
  chain_ok: boolean
}

export type Approval = {
  id: string
  agent: string
  tool: string
  summary: string
  amount_cents: number | null
  currency: string | null
  reason: string
  args: Record<string, unknown>
  status: 'pending' | 'approved' | 'rejected'
  created_at: string
}

export type LedgerEntry = {
  id: number
  kind: 'event' | 'decision' | 'agent_step' | 'approval' | 'note'
  subject_id: string
  summary: string
  payload: unknown
  prev_hash: string
  hash: string
  created_at: string
}

export type Verify = { ok: boolean; checked: number; broken_at: number | null }

export type Run = {
  id: string
  agent: string
  event_type: string
  status: string
  started_at: string
  steps: { kind: 'llm' | 'tool' | 'note'; summary: string }[]
  output: unknown
}

export type Fact = { claim: string; ledger_entry_id: number }

export type EvidencePack = {
  dispute_id: string
  reason: string
  classification: 'friendly_fraud' | 'genuine' | 'unclear'
  confidence: number
  checklist: Record<string, boolean>
  facts: Fact[]
  note_to_paypal: string
  recommended_action: 'provide_evidence' | 'offer_refund' | 'accept_claim'
}

export type SentinelVerdict = {
  verdict: 'scam' | 'legit' | 'unsure'
  confidence: number
  matched_payment_entry_id: number | null
  red_flags: string[]
  explanation: string
}

export type HealthReport = {
  score: number
  factors: { name: string; value: unknown; impact: string; note: string }[]
  recommendations: string[]
  appeal_pack: string | null
}