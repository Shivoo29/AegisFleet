# Summary (/docs/api/openapi/console/summary)

`GET /api/summary`

Overview numbers: money waiting on approval, open disputes, overdue invoices, health, chain state.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/summary:
    get:
      tags:
        - console
      summary: Summary
      description: "Overview numbers: money waiting on approval, open disputes,
        overdue invoices, health, chain state."
      operationId: summary
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Summary"
        "401":
          description: "Login required: HTTP Basic or the session cookie"
      security:
        - HTTPBasic: []
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.ConsoleApi.Summary();
                  // TODO: Handle 'response' of type Summary
              }
              catch (ApiException<SummaryError> ex)
              {
                  if (ex.Error.TryGetNoContent(out var error))
                  {
                      // TODO: Handle 'error' of type RawError
                  }
              }
        - lang: python
          label: Python
          sources:
            Example: |-
              try:
                  response = client.console.summary()
                  # TODO: Handle 'response' of type Summary
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type SummaryErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.summary();
                // TODO: Handle 'response' of type Summary
              } catch (err) {
                // TODO: Handle 'err' of type Console.SummaryError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    Summary:
      properties:
        money_at_risk_cents:
          type: integer
          description: Total held for approval, in cents
        currency:
          type: string
          description: ISO 4217 currency code
        pending_approvals:
          type: integer
          description: Actions waiting for a human
        open_disputes:
          type: integer
          description: Number of open disputes
        overdue_invoices:
          type: integer
          description: Number of overdue invoice events
        health_score:
          type: integer
          description: Account health score, 0-100
        kill_switch:
          type: boolean
          description: True when the kill switch blocks all agent actions
        chain_ok:
          type: boolean
          description: True when every ledger hash still matches
      type: object
      required:
        - money_at_risk_cents
        - currency
        - pending_approvals
        - open_disputes
        - overdue_invoices
        - health_score
        - kill_switch
        - chain_ok
      title: Summary
      description: Summary object
info:
  title: AegisFleet
  version: 1.0.0
```