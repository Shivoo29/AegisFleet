# Ledger Verify (/docs/api/openapi/console/ledger_verify)

`GET /api/ledger/verify`

Recompute every hash in the chain and report the first entry that no longer matches.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/ledger/verify:
    get:
      tags:
        - console
      summary: Ledger Verify
      description: Recompute every hash in the chain and report the first entry that
        no longer matches.
      operationId: ledger_verify
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ChainVerify"
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
                  var response = await client.ConsoleApi.LedgerVerify();
                  // TODO: Handle 'response' of type ChainVerify
              }
              catch (ApiException<LedgerVerifyError> ex)
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
                  response = client.console.ledger_verify()
                  # TODO: Handle 'response' of type ChainVerify
              except ApiError as e:
                  # TODO: Handle 'e.error' of type LedgerVerifyErrorBody
                  ...
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.ledgerVerify();
                // TODO: Handle 'response' of type ChainVerify
              } catch (err) {
                // TODO: Handle 'err' of type Console.LedgerVerifyError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    ChainVerify:
      properties:
        ok:
          type: boolean
          description: True on success
        checked:
          type: integer
          description: Number of ledger entries checked
        broken_at:
          anyOf:
            - type: integer
              description: First ledger id whose hash no longer matches
            - type: "null"
              description: Not set
          description: First ledger id whose hash no longer matches
      type: object
      required:
        - ok
        - checked
      title: ChainVerify
      description: ChainVerify object
info:
  title: AegisFleet
  version: 1.0.0
```