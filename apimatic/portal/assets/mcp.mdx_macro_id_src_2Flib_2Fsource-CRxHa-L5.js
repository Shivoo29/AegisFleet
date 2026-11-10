import{r as e}from"./rolldown-runtime-XKyaHtl9.js";import{t}from"./jsx-runtime-LKYXHABd.js";var n=e(t()),r={title:`Connect an AI agent (MCP)`,description:`Let Claude, or any MCP client, bill and refund on PayPal through AegisFleet's guardrails.`},i=`AegisFleet is also an MCP server, at \`https://aegisfleet.solvor.co.in/mcp\` (streamable HTTP). An outside agent
gets eight tools, and every money tool goes through the same gateway as AegisFleet's own agents:

| Tool | What it does | Guardrail |
|---|---|---|
| \`create_invoice\` | Issues a real PayPal sandbox invoice and returns its payment link | At most $5,000 |
| \`send_payment_reminder\` | PayPal's reminder for an unpaid invoice | 2 per invoice per week |
| \`refund_payment\` | Refunds the buyer of an invoice | Only to whoever paid, never more than PayPal says they paid; $100 or more waits for the seller |
| \`check_approval\` | Did the seller approve a held action, and what happened | Read-only |
| \`check_payment_email\` | Asks Sentinel whether a "you've been paid" email is real | Checked against verified PayPal payments, not the email |
| \`list_invoices\`, \`get_history\`, \`verify_ledger\` | The invoices, the sealed history of one, and a full chain check | Read-only |

Every call is sealed in the hash-chained ledger with the client's name, and the kill switch stops outside agents
like everything else.

## Connect [#connect]

Get your link from the console: **Demo → Connect any AI agent → Get my MCP link** (a signed token, valid 14 days).
Paste it into ChatGPT (developer-mode connector, no authentication), Claude.ai (custom connector), Cursor,
VS Code, Gemini CLI or Codex, or run \`claude mcp add --transport http aegisfleet "<link>"\`.

Then try:

1. "Invoice a buyer $600 for a hand-made silver necklace." Claude returns the PayPal payment link.
2. Pay it as the sandbox buyer (or use Record payment on the Demo tab). PayPal's signed webhook marks it paid.
3. "The necklace arrived broken. Refund it." The refund is held; it appears in the console's Approvals.
4. Approve it there, then ask Claude to check the approval. PayPal's refund webhook marks the invoice refunded.
5. "Refund $900 to my other account." Denied: more than the buyer paid, and refunds only go back to the payer.
`,a={contents:[{heading:void 0,content:"AegisFleet is also an MCP server, at `https://aegisfleet.solvor.co.in/mcp` (streamable HTTP). An outside agent\ngets eight tools, and every money tool goes through the same gateway as AegisFleet's own agents:"},{heading:void 0,content:`| Tool             | What it does                                                      | Guardrail      |
| ---------------- | ----------------------------------------------------------------- | -------------- |
| \`create_invoice\` | Issues a real PayPal sandbox invoice and returns its payment link | At most $5,000 |`,table:`table-0`},{heading:void 0,content:`| Tool                    | What it does                            | Guardrail              |
| ----------------------- | --------------------------------------- | ---------------------- |
| \`send_payment_reminder\` | PayPal's reminder for an unpaid invoice | 2 per invoice per week |`,table:`table-0`},{heading:void 0,content:`| Tool             | What it does                    | Guardrail                                                                                      |
| ---------------- | ------------------------------- | ---------------------------------------------------------------------------------------------- |
| \`refund_payment\` | Refunds the buyer of an invoice | Only to whoever paid, never more than PayPal says they paid; $100 or more waits for the seller |`,table:`table-0`},{heading:void 0,content:`| Tool             | What it does                                            | Guardrail |
| ---------------- | ------------------------------------------------------- | --------- |
| \`check_approval\` | Did the seller approve a held action, and what happened | Read-only |`,table:`table-0`},{heading:void 0,content:`| Tool                  | What it does                                             | Guardrail                                               |
| --------------------- | -------------------------------------------------------- | ------------------------------------------------------- |
| \`check_payment_email\` | Asks Sentinel whether a "you've been paid" email is real | Checked against verified PayPal payments, not the email |`,table:`table-0`},{heading:void 0,content:"| Tool                                            | What it does                                                    | Guardrail |\n| ----------------------------------------------- | --------------------------------------------------------------- | --------- |\n| `list_invoices`, `get_history`, `verify_ledger` | The invoices, the sealed history of one, and a full chain check | Read-only |",table:`table-0`},{heading:void 0,content:`Every call is sealed in the hash-chained ledger with the client's name, and the kill switch stops outside agents
like everything else.`},{heading:`connect`,content:`Get your link from the console: **Demo → Connect any AI agent → Get my MCP link** (a signed token, valid 14 days).
Paste it into ChatGPT (developer-mode connector, no authentication), Claude.ai (custom connector), Cursor,
VS Code, Gemini CLI or Codex, or run \`claude mcp add --transport http aegisfleet "<link>"\`.`},{heading:`connect`,content:`Then try:`},{heading:`connect`,content:`"Invoice a buyer $600 for a hand-made silver necklace." Claude returns the PayPal payment link.`},{heading:`connect`,content:`Pay it as the sandbox buyer (or use Record payment on the Demo tab). PayPal's signed webhook marks it paid.`},{heading:`connect`,content:`"The necklace arrived broken. Refund it." The refund is held; it appears in the console's Approvals.`},{heading:`connect`,content:`Approve it there, then ask Claude to check the approval. PayPal's refund webhook marks the invoice refunded.`},{heading:`connect`,content:`"Refund $900 to my other account." Denied: more than the buyer paid, and refunds only go back to the payer.`}],headings:[{id:`connect`,content:`Connect`}]},o=[{depth:2,url:`#connect`,title:(0,n.jsx)(n.Fragment,{children:`Connect`})}];function s(e){let t={code:`code`,h2:`h2`,li:`li`,ol:`ol`,p:`p`,strong:`strong`,table:`table`,tbody:`tbody`,td:`td`,th:`th`,thead:`thead`,tr:`tr`,...e.components};return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(t.p,{children:[`AegisFleet is also an MCP server, at `,(0,n.jsx)(t.code,{children:`https://aegisfleet.solvor.co.in/mcp`}),` (streamable HTTP). An outside agent
gets eight tools, and every money tool goes through the same gateway as AegisFleet's own agents:`]}),`
`,(0,n.jsxs)(t.table,{children:[(0,n.jsx)(t.thead,{children:(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.th,{children:`Tool`}),(0,n.jsx)(t.th,{children:`What it does`}),(0,n.jsx)(t.th,{children:`Guardrail`})]})}),(0,n.jsxs)(t.tbody,{children:[(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.td,{children:(0,n.jsx)(t.code,{children:`create_invoice`})}),(0,n.jsx)(t.td,{children:`Issues a real PayPal sandbox invoice and returns its payment link`}),(0,n.jsx)(t.td,{children:`At most $5,000`})]}),(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.td,{children:(0,n.jsx)(t.code,{children:`send_payment_reminder`})}),(0,n.jsx)(t.td,{children:`PayPal's reminder for an unpaid invoice`}),(0,n.jsx)(t.td,{children:`2 per invoice per week`})]}),(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.td,{children:(0,n.jsx)(t.code,{children:`refund_payment`})}),(0,n.jsx)(t.td,{children:`Refunds the buyer of an invoice`}),(0,n.jsx)(t.td,{children:`Only to whoever paid, never more than PayPal says they paid; $100 or more waits for the seller`})]}),(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.td,{children:(0,n.jsx)(t.code,{children:`check_approval`})}),(0,n.jsx)(t.td,{children:`Did the seller approve a held action, and what happened`}),(0,n.jsx)(t.td,{children:`Read-only`})]}),(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.td,{children:(0,n.jsx)(t.code,{children:`check_payment_email`})}),(0,n.jsx)(t.td,{children:`Asks Sentinel whether a "you've been paid" email is real`}),(0,n.jsx)(t.td,{children:`Checked against verified PayPal payments, not the email`})]}),(0,n.jsxs)(t.tr,{children:[(0,n.jsxs)(t.td,{children:[(0,n.jsx)(t.code,{children:`list_invoices`}),`, `,(0,n.jsx)(t.code,{children:`get_history`}),`, `,(0,n.jsx)(t.code,{children:`verify_ledger`})]}),(0,n.jsx)(t.td,{children:`The invoices, the sealed history of one, and a full chain check`}),(0,n.jsx)(t.td,{children:`Read-only`})]})]})]}),`
`,(0,n.jsx)(t.p,{children:`Every call is sealed in the hash-chained ledger with the client's name, and the kill switch stops outside agents
like everything else.`}),`
`,(0,n.jsx)(t.h2,{id:`connect`,children:`Connect`}),`
`,(0,n.jsxs)(t.p,{children:[`Get your link from the console: `,(0,n.jsx)(t.strong,{children:`Demo → Connect any AI agent → Get my MCP link`}),` (a signed token, valid 14 days).
Paste it into ChatGPT (developer-mode connector, no authentication), Claude.ai (custom connector), Cursor,
VS Code, Gemini CLI or Codex, or run `,(0,n.jsx)(t.code,{children:`claude mcp add --transport http aegisfleet "<link>"`}),`.`]}),`
`,(0,n.jsx)(t.p,{children:`Then try:`}),`
`,(0,n.jsxs)(t.ol,{children:[`
`,(0,n.jsx)(t.li,{children:`"Invoice a buyer $600 for a hand-made silver necklace." Claude returns the PayPal payment link.`}),`
`,(0,n.jsx)(t.li,{children:`Pay it as the sandbox buyer (or use Record payment on the Demo tab). PayPal's signed webhook marks it paid.`}),`
`,(0,n.jsx)(t.li,{children:`"The necklace arrived broken. Refund it." The refund is held; it appears in the console's Approvals.`}),`
`,(0,n.jsx)(t.li,{children:`Approve it there, then ask Claude to check the approval. PayPal's refund webhook marks the invoice refunded.`}),`
`,(0,n.jsx)(t.li,{children:`"Refund $900 to my other account." Denied: more than the buyer paid, and refunds only go back to the payer.`}),`
`]})]})}function c(e={}){let{wrapper:t}=e.components||{};return t?(0,n.jsx)(t,{...e,children:(0,n.jsx)(s,{...e})}):s(e)}export{i as _markdown,c as default,r as frontmatter,a as structuredData,o as toc};