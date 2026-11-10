# Invoices (/docs/api/openapi/console/invoices)

`GET /api/invoices`

Invoices with paid/overdue status, risk, shipment and PayPal payment link.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/invoices:
    get:
      tags:
        - console
      summary: Invoices
      description: Invoices with paid/overdue status, risk, shipment and PayPal
        payment link.
      operationId: invoices
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                items:
                  $ref: "#/components/schemas/Invoice"
                type: array
                title: Response 200 Invoices
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
                  var response = await client.ConsoleApi.Invoices();
                  // TODO: Handle 'response' of type IReadOnlyList<Invoice>
              }
              catch (ApiException<InvoicesError> ex)
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
                  response = client.console.invoices()
                  # TODO: Handle 'response' of type list[Invoice]
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type InvoicesErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.invoices();
                // TODO: Handle 'response' of type Invoice[]
              } catch (err) {
                // TODO: Handle 'err' of type Console.InvoicesError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    Invoice:
      properties:
        id:
          type: string
          description: Unique id
        buyer_email:
          anyOf:
            - type: string
              description: Buyer's email address
            - type: "null"
              description: Not set
          description: Buyer's email address
        amount_cents:
          anyOf:
            - type: integer
              description: Amount in minor units (cents)
            - type: "null"
              description: Not set
          description: Amount in minor units (cents)
        currency:
          type: string
          description: ISO 4217 currency code
        status:
          type: string
          enum:
            - paid
            - overdue
            - sent
          description: Current status
        days_overdue:
          type: integer
          description: Days past the due date; 0 when paid or not yet due
        risk:
          type: string
          enum:
            - low
            - medium
            - high
          description: "Payment risk: low, medium or high"
        shipped:
          type: boolean
          description: True when tracking was added
        tracking_number:
          anyOf:
            - type: string
              description: Carrier tracking number
            - type: "null"
              description: Not set
          description: Carrier tracking number
        created_at:
          anyOf:
            - type: string
              description: When it was created (ISO 8601)
            - type: "null"
              description: Not set
          description: When it was created (ISO 8601)
        paid_at:
          anyOf:
            - type: string
              format: date-time
              description: When payment was verified (ISO 8601)
            - type: "null"
              description: Not set
          description: When payment was verified (ISO 8601)
        pay_url:
          anyOf:
            - type: string
              description: PayPal payment page for this invoice
            - type: "null"
              description: Not set
          description: PayPal payment page for this invoice
      type: object
      required:
        - id
        - currency
        - status
        - days_overdue
        - risk
        - shipped
      title: Invoice
      description: Invoice object
info:
  title: AegisFleet
  version: 1.0.0
```