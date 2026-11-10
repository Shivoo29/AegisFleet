# Ledger (/docs/api/openapi/console/ledger)

`GET /api/ledger`

Proof Ledger entries, newest first. Each entry's hash covers the previous one.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/ledger:
    get:
      tags:
        - console
      summary: Ledger
      description: Proof Ledger entries, newest first. Each entry's hash covers the
        previous one.
      operationId: ledger
      security:
        - HTTPBasic: []
      parameters:
        - name: kind
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                description: "Entry kind: event, decision, agent_step, approval or note"
              - type: "null"
                description: Not set
            description: "Entry kind: event, decision, agent_step, approval or note"
          description: "Entry kind: event, decision, agent_step, approval or note"
        - name: subject_id
          in: query
          required: false
          schema:
            anyOf:
              - type: string
                description: "What this is about: an invoice, dispute or email id"
              - type: "null"
                description: Not set
            description: "What this is about: an invoice, dispute or email id"
          description: "What this is about: an invoice, dispute or email id"
        - name: limit
          in: query
          required: false
          schema:
            type: integer
            default: 100
            description: Maximum number of items to return
          description: Maximum number of items to return
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: "#/components/schemas/LedgerEntry"
                title: Response 200 Ledger
        "401":
          description: "Login required: HTTP Basic or the session cookie"
        "422":
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.ConsoleApi.Ledger(
                      new LedgerRequest());
                  // TODO: Handle 'response' of type IReadOnlyList<LedgerEntry>
              }
              catch (ApiException<LedgerError> ex)
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
                  response = client.console.ledger()
                  # TODO: Handle 'response' of type list[LedgerEntry]
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type LedgerErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.ledger();
                // TODO: Handle 'response' of type LedgerEntry[]
              } catch (err) {
                // TODO: Handle 'err' of type Console.LedgerError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    LedgerEntry:
      properties:
        id:
          type: integer
          description: Unique id
        kind:
          type: string
          enum:
            - event
            - decision
            - agent_step
            - approval
            - note
          description: "Entry kind: event, decision, agent_step, approval or note"
        subject_id:
          type: string
          description: "What this is about: an invoice, dispute or email id"
        summary:
          type: string
          description: One-line summary
        payload:
          type: object
          description: Sealed data for this entry
        prev_hash:
          type: string
          description: Hash of the previous entry; empty for the first
        hash:
          type: string
          description: SHA-256 of this entry plus the previous hash
        created_at:
          type: string
          format: date-time
          description: When it was created (ISO 8601)
      type: object
      required:
        - id
        - kind
        - subject_id
        - summary
        - payload
        - prev_hash
        - hash
        - created_at
      title: LedgerEntry
      description: LedgerEntry object
    HTTPValidationError:
      properties:
        detail:
          items:
            $ref: "#/components/schemas/ValidationError"
          type: array
          description: Validation errors
      type: object
      title: HTTPValidationError
      description: HTTPValidationError object
    ValidationError:
      properties:
        loc:
          items:
            anyOf:
              - type: string
              - type: integer
          type: array
          description: Where the invalid value is
        msg:
          type: string
          description: Error message
        type:
          type: string
          description: Error type
      type: object
      required:
        - loc
        - msg
        - type
      title: ValidationError
      description: ValidationError object
info:
  title: AegisFleet
  version: 1.0.0
```