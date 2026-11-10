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

## Claude Code [#claude-code]

\`\`\`
claude mcp add --transport http aegisfleet https://aegisfleet.solvor.co.in/mcp \\
  --header "Authorization: Basic <base64 of user:password>"
\`\`\`

The console's Demo tab builds this command for you. Then try:

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
like everything else.`},{heading:`claude-code`,content:`The console's Demo tab builds this command for you. Then try:`},{heading:`claude-code`,content:`"Invoice a buyer $600 for a hand-made silver necklace." Claude returns the PayPal payment link.`},{heading:`claude-code`,content:`Pay it as the sandbox buyer (or use Record payment on the Demo tab). PayPal's signed webhook marks it paid.`},{heading:`claude-code`,content:`"The necklace arrived broken. Refund it." The refund is held; it appears in the console's Approvals.`},{heading:`claude-code`,content:`Approve it there, then ask Claude to check the approval. PayPal's refund webhook marks the invoice refunded.`},{heading:`claude-code`,content:`"Refund $900 to my other account." Denied: more than the buyer paid, and refunds only go back to the payer.`}],headings:[{id:`claude-code`,content:`Claude Code`}]},o=[{depth:2,url:`#claude-code`,title:(0,n.jsx)(n.Fragment,{children:`Claude Code`})}];function s(e){let t={code:`code`,h2:`h2`,li:`li`,ol:`ol`,p:`p`,pre:`pre`,span:`span`,table:`table`,tbody:`tbody`,td:`td`,th:`th`,thead:`thead`,tr:`tr`,...e.components};return(0,n.jsxs)(n.Fragment,{children:[(0,n.jsxs)(t.p,{children:[`AegisFleet is also an MCP server, at `,(0,n.jsx)(t.code,{children:`https://aegisfleet.solvor.co.in/mcp`}),` (streamable HTTP). An outside agent
gets eight tools, and every money tool goes through the same gateway as AegisFleet's own agents:`]}),`
`,(0,n.jsxs)(t.table,{children:[(0,n.jsx)(t.thead,{children:(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.th,{children:`Tool`}),(0,n.jsx)(t.th,{children:`What it does`}),(0,n.jsx)(t.th,{children:`Guardrail`})]})}),(0,n.jsxs)(t.tbody,{children:[(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.td,{children:(0,n.jsx)(t.code,{children:`create_invoice`})}),(0,n.jsx)(t.td,{children:`Issues a real PayPal sandbox invoice and returns its payment link`}),(0,n.jsx)(t.td,{children:`At most $5,000`})]}),(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.td,{children:(0,n.jsx)(t.code,{children:`send_payment_reminder`})}),(0,n.jsx)(t.td,{children:`PayPal's reminder for an unpaid invoice`}),(0,n.jsx)(t.td,{children:`2 per invoice per week`})]}),(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.td,{children:(0,n.jsx)(t.code,{children:`refund_payment`})}),(0,n.jsx)(t.td,{children:`Refunds the buyer of an invoice`}),(0,n.jsx)(t.td,{children:`Only to whoever paid, never more than PayPal says they paid; $100 or more waits for the seller`})]}),(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.td,{children:(0,n.jsx)(t.code,{children:`check_approval`})}),(0,n.jsx)(t.td,{children:`Did the seller approve a held action, and what happened`}),(0,n.jsx)(t.td,{children:`Read-only`})]}),(0,n.jsxs)(t.tr,{children:[(0,n.jsx)(t.td,{children:(0,n.jsx)(t.code,{children:`check_payment_email`})}),(0,n.jsx)(t.td,{children:`Asks Sentinel whether a "you've been paid" email is real`}),(0,n.jsx)(t.td,{children:`Checked against verified PayPal payments, not the email`})]}),(0,n.jsxs)(t.tr,{children:[(0,n.jsxs)(t.td,{children:[(0,n.jsx)(t.code,{children:`list_invoices`}),`, `,(0,n.jsx)(t.code,{children:`get_history`}),`, `,(0,n.jsx)(t.code,{children:`verify_ledger`})]}),(0,n.jsx)(t.td,{children:`The invoices, the sealed history of one, and a full chain check`}),(0,n.jsx)(t.td,{children:`Read-only`})]})]})]}),`
`,(0,n.jsx)(t.p,{children:`Every call is sealed in the hash-chained ledger with the client's name, and the kill switch stops outside agents
like everything else.`}),`
`,(0,n.jsx)(t.h2,{id:`claude-code`,children:`Claude Code`}),`
`,(0,n.jsx)(n.Fragment,{children:(0,n.jsx)(t.pre,{className:`shiki shiki-themes github-light github-dark`,style:{"--shiki-light":`#24292e`,"--shiki-dark":`#e1e4e8`,"--shiki-light-bg":`#fff`,"--shiki-dark-bg":`#24292e`},tabIndex:`0`,icon:`<svg viewBox="0 0 24 24"><path d="M 6,1 C 4.354992,1 3,2.354992 3,4 v 16 c 0,1.645008 1.354992,3 3,3 h 12 c 1.645008,0 3,-1.354992 3,-3 V 8 7 A 1.0001,1.0001 0 0 0 20.707031,6.2929687 l -5,-5 A 1.0001,1.0001 0 0 0 15,1 h -1 z m 0,2 h 7 v 3 c 0,1.645008 1.354992,3 3,3 h 3 v 11 c 0,0.564129 -0.435871,1 -1,1 H 6 C 5.4358712,21 5,20.564129 5,20 V 4 C 5,3.4358712 5.4358712,3 6,3 Z M 15,3.4140625 18.585937,7 H 16 C 15.435871,7 15,6.5641288 15,6 Z" fill="currentColor" /></svg>`,children:(0,n.jsxs)(t.code,{children:[(0,n.jsx)(t.span,{className:`line`,children:(0,n.jsx)(t.span,{children:`claude mcp add --transport http aegisfleet https://aegisfleet.solvor.co.in/mcp \\`})}),`
`,(0,n.jsx)(t.span,{className:`line`,children:(0,n.jsx)(t.span,{children:`  --header "Authorization: Basic <base64 of user:password>"`})})]})})}),`
`,(0,n.jsx)(t.p,{children:`The console's Demo tab builds this command for you. Then try:`}),`
`,(0,n.jsxs)(t.ol,{children:[`
`,(0,n.jsx)(t.li,{children:`"Invoice a buyer $600 for a hand-made silver necklace." Claude returns the PayPal payment link.`}),`
`,(0,n.jsx)(t.li,{children:`Pay it as the sandbox buyer (or use Record payment on the Demo tab). PayPal's signed webhook marks it paid.`}),`
`,(0,n.jsx)(t.li,{children:`"The necklace arrived broken. Refund it." The refund is held; it appears in the console's Approvals.`}),`
`,(0,n.jsx)(t.li,{children:`Approve it there, then ask Claude to check the approval. PayPal's refund webhook marks the invoice refunded.`}),`
`,(0,n.jsx)(t.li,{children:`"Refund $900 to my other account." Denied: more than the buyer paid, and refunds only go back to the payer.`}),`
`]})]})}function c(e={}){let{wrapper:t}=e.components||{};return t?(0,n.jsx)(t,{...e,children:(0,n.jsx)(s,{...e})}):s(e)}export{i as _markdown,c as default,r as frontmatter,a as structuredData,o as toc};