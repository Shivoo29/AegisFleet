/** Inlined mock payloads — no dynamic JSON imports (Vite-safe). */

export const summaryMock = {
  money_at_risk_cents: 60000,
  currency: 'USD',
  pending_approvals: 1,
  open_disputes: 1,
  overdue_invoices: 1,
  health_score: 82,
  kill_switch: false,
  chain_ok: true,
}

export const approvalsMock = [
  {
    id: 'apr_7',
    agent: 'defender',
    tool: 'provide_dispute_evidence',
    summary: 'Submit evidence for dispute PP-D-12345',
    amount_cents: 60000,
    currency: 'USD',
    reason:
      'Buyer claims item not received. Sealed tracking shows delivered to the matching address.',
    args: { dispute_id: 'PP-D-12345' },
    status: 'pending' as const,
    created_at: '2026-11-05T10:22:31Z',
  },
  {
    id: 'apr_6',
    agent: 'collector',
    tool: 'send_invoice_reminder',
    summary: 'Send second reminder for INV-0007',
    amount_cents: 60000,
    currency: 'USD',
    reason: 'First reminder was sent 3 days ago; client has not replied.',
    args: { invoice_id: 'INV-0007', tone: 'firm' },
    status: 'pending' as const,
    created_at: '2026-11-05T09:15:00Z',
  },
]

export const runsMock = [
  {
    id: 'run_19',
    agent: 'sentinel',
    event_type: 'email.received',
    status: 'done',
    started_at: '2026-11-05T10:20:02Z',
    steps: [
      { kind: 'tool' as const, summary: 'ledger.find: no verified payment for INV-0007' },
      { kind: 'llm' as const, summary: 'verdict: scam (confidence 0.93)' },
      { kind: 'note' as const, summary: 'Ship gate kept closed; seller notified in console' },
    ],
    output: {
      verdict: 'scam',
      confidence: 0.93,
      red_flags: [
        'sender domain is not paypal.com',
        'no matching verified payment in ledger',
      ],
    },
  },
  {
    id: 'run_18',
    agent: 'defender',
    event_type: 'dispute.created',
    status: 'done',
    started_at: '2026-11-05T10:22:10Z',
    steps: [
      { kind: 'tool' as const, summary: 'ledger: pulled tracking + delivery proof for INV-0007' },
      { kind: 'llm' as const, summary: 'classification: friendly_fraud (0.88)' },
      {
        kind: 'tool' as const,
        summary: 'gateway: provide_dispute_evidence → HOLD (needs approval)',
      },
    ],
    output: {
      dispute_id: 'PP-D-12345',
      classification: 'friendly_fraud',
      recommended_action: 'provide_evidence',
    },
  },
  {
    id: 'run_17',
    agent: 'collector',
    event_type: 'invoice.overdue',
    status: 'done',
    started_at: '2026-11-04T09:00:00Z',
    steps: [
      { kind: 'llm' as const, summary: 'tone selected: polite (first reminder)' },
      { kind: 'tool' as const, summary: 'send_invoice_reminder for INV-0007' },
    ],
    output: { reminder_number: 1, tone: 'polite' },
  },
  {
    id: 'run_16',
    agent: 'guardian',
    event_type: 'payment.captured',
    status: 'done',
    started_at: '2026-11-05T11:02:20Z',
    steps: [
      { kind: 'tool' as const, summary: 'webhook signature verified' },
      { kind: 'tool' as const, summary: 'ledger.seal: payment PAY-9X2K for INV-0007' },
      { kind: 'note' as const, summary: 'Ship gate opened' },
    ],
    output: { capture_id: 'PAY-9X2K', amount_cents: 60000 },
  },
]

export const ledgerMock = [
  {
    id: 12,
    kind: 'event' as const,
    subject_id: 'INV-0007',
    summary: 'Invoice INV-0007 sent to client@example.com for $600.00',
    payload: { invoice_id: 'INV-0007', amount_cents: 60000, currency: 'USD' },
    prev_hash: '0'.repeat(64),
    hash: 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456',
    created_at: '2026-11-03T08:12:00Z',
  },
  {
    id: 13,
    kind: 'agent_step' as const,
    subject_id: 'INV-0007',
    summary: 'Collector sent polite reminder #1 for INV-0007',
    payload: { agent: 'collector', tone: 'polite', channel: 'email' },
    prev_hash: 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456',
    hash: 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef12345678',
    created_at: '2026-11-04T09:00:11Z',
  },
  {
    id: 14,
    kind: 'event' as const,
    subject_id: 'email-scam-01',
    summary: 'Email received from paypa1-support.com claiming payment for INV-0007',
    payload: {
      from: 'support@paypa1-support.com',
      subject: 'Payment received — ship now',
    },
    prev_hash: 'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef12345678',
    hash: 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890',
    created_at: '2026-11-05T10:19:44Z',
  },
  {
    id: 15,
    kind: 'decision' as const,
    subject_id: 'email-scam-01',
    summary:
      'Sentinel flagged fake payment email from paypa1-support.com (confidence 0.93)',
    payload: {
      verdict: 'scam',
      red_flags: [
        'sender domain is not paypal.com',
        'no matching verified payment in ledger',
      ],
      agent: 'sentinel',
    },
    prev_hash: 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef1234567890',
    hash: 'd4e5f6789012345678901234567890abcdef1234567890abcdef123456789012',
    created_at: '2026-11-05T10:20:05Z',
  },
  {
    id: 16,
    kind: 'event' as const,
    subject_id: 'PAY-9X2K',
    summary: 'Payment captured $600.00 USD for INV-0007 (webhook verified)',
    payload: {
      capture_id: 'PAY-9X2K',
      amount_cents: 60000,
      currency: 'USD',
      invoice_id: 'INV-0007',
    },
    prev_hash: 'd4e5f6789012345678901234567890abcdef1234567890abcdef123456789012',
    hash: 'e5f6789012345678901234567890abcdef1234567890abcdef12345678901234',
    created_at: '2026-11-05T11:02:18Z',
  },
  {
    id: 17,
    kind: 'approval' as const,
    subject_id: 'PP-D-12345',
    summary: 'Defender requests approval to submit evidence for dispute PP-D-12345',
    payload: {
      agent: 'defender',
      tool: 'provide_dispute_evidence',
      amount_cents: 60000,
    },
    prev_hash: 'e5f6789012345678901234567890abcdef1234567890abcdef12345678901234',
    hash: 'f6789012345678901234567890abcdef1234567890abcdef1234567890123456',
    created_at: '2026-11-05T10:22:40Z',
  },
]

export const verifyMock = {
  ok: true,
  checked: 6,
  broken_at: null as number | null,
}

export const healthMock = {
  score: 82,
  factors: [
    {
      name: 'tracking_present',
      value: true,
      impact: 'positive',
      note: 'Shipment tracking was added within 24h of capture',
    },
    {
      name: 'delivery_confirmed',
      value: false,
      impact: 'neutral',
      note: 'Awaiting courier delivery scan',
    },
    {
      name: 'dispute_open',
      value: true,
      impact: 'negative',
      note: "One open 'item not received' dispute",
    },
  ],
  recommendations: [
    'Confirm delivery status with the courier',
    'Keep the sealed evidence pack ready for the dispute response',
  ],
  appeal_pack: null as string | null,
}

export const disputesMock = [
  {
    id: 'PP-D-12345',
    invoice_id: 'INV-0007',
    reason: 'ITEM_NOT_RECEIVED',
    status: 'WAITING_FOR_SELLER_RESPONSE',
    amount_cents: 60000,
    currency: 'USD',
    buyer_name: 'Alex M.',
    created_at: '2026-11-05T10:21:00Z',
    due_by: '2026-11-12T10:21:00Z',
  },
]

export const disputeDetailMock = {
  dispute: {
    id: 'PP-D-12345',
    invoice_id: 'INV-0007',
    reason: 'ITEM_NOT_RECEIVED',
    status: 'WAITING_FOR_SELLER_RESPONSE',
    amount_cents: 60000,
    currency: 'USD',
    buyer_name: 'Alex M.',
    created_at: '2026-11-05T10:21:00Z',
    due_by: '2026-11-12T10:21:00Z',
  },
  evidence_pack: {
    dispute_id: 'PP-D-12345',
    reason: 'ITEM_NOT_RECEIVED',
    classification: 'friendly_fraud' as const,
    confidence: 0.88,
    checklist: {
      online_verifiable_tracking: true,
      delivered_status: true,
      recipient_address_match: true,
      shipped_within_timeframe: true,
      item_description_match: true,
    },
    facts: [
      {
        claim: 'Tracking number was sealed in the ledger at shipment time',
        ledger_entry_id: 16,
      },
      {
        claim: 'Courier marked the package as delivered to the matching address',
        ledger_entry_id: 16,
      },
      {
        claim: 'Payment of $600.00 USD was verified via PayPal webhook',
        ledger_entry_id: 16,
      },
    ],
    note_to_paypal:
      "The item (custom necklace, INV-0007) was shipped with online-verifiable tracking and marked delivered to the address on the order. All proof is sealed in our Proof Ledger. We request the dispute be resolved in the seller's favour under Seller Protection.",
    recommended_action: 'provide_evidence' as const,
  },
  approval_id: 'apr_7',
}