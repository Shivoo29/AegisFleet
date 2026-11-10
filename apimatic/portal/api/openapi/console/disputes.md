# Disputes (/docs/api/openapi/console/disputes)

`GET /api/disputes`

Latest state of every PayPal dispute, newest first.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/disputes:
    get:
      tags:
        - console
      summary: Disputes
      description: Latest state of every PayPal dispute, newest first.
      operationId: disputes
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                items:
                  $ref: "#/components/schemas/Dispute"
                type: array
                title: Response 200 Disputes
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
                  var response = await client.ConsoleApi.Disputes();
                  // TODO: Handle 'response' of type IReadOnlyList<Dispute>
              }
              catch (ApiException<DisputesError> ex)
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
                  response = client.console.disputes()
                  # TODO: Handle 'response' of type list[Dispute]
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type DisputesErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.disputes();
                // TODO: Handle 'response' of type Dispute[]
              } catch (err) {
                // TODO: Handle 'err' of type Console.DisputesError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    Dispute:
      properties:
        id:
          type: string
          description: Unique id
        invoice_id:
          anyOf:
            - type: string
              description: Invoice id, e.g. INV-0007
            - type: "null"
              description: Not set
          description: Invoice id, e.g. INV-0007
        reason:
          type: string
          description: Why
        status:
          type: string
          description: Current status
        amount_cents:
          anyOf:
            - type: integer
              description: Amount in minor units (cents)
            - type: "null"
              description: Not set
          description: Amount in minor units (cents)
        currency:
          anyOf:
            - type: string
              description: ISO 4217 currency code
            - type: "null"
              description: Not set
          description: ISO 4217 currency code
        buyer_name:
          anyOf:
            - type: string
              description: Buyer's name as PayPal reports it
            - type: "null"
              description: Not set
          description: Buyer's name as PayPal reports it
        created_at:
          type: string
          format: date-time
          description: When it was created (ISO 8601)
        due_by:
          anyOf:
            - type: string
              description: Seller response deadline (ISO 8601)
            - type: "null"
              description: Not set
          description: Seller response deadline (ISO 8601)
      type: object
      required:
        - id
        - reason
        - status
        - created_at
      title: Dispute
      description: Dispute object
info:
  title: AegisFleet
  version: 1.0.0
```