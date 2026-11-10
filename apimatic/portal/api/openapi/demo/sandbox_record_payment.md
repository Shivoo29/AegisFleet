# Sandbox Record Payment (/docs/api/openapi/demo/sandbox_record_payment)

`POST /api/demo/sandbox_record_payment`

Backup for flaky sandbox checkout: record payment on the newest unpaid sandbox invoice.

PayPal then sends the same signed INVOICING.INVOICE.PAID webhook a buyer payment would.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/demo/sandbox_record_payment:
    post:
      tags:
        - demo
      summary: Sandbox Record Payment
      description: >-
        Backup for flaky sandbox checkout: record payment on the newest unpaid
        sandbox invoice.


        PayPal then sends the same signed INVOICING.INVOICE.PAID webhook a buyer
        payment would.
      operationId: sandbox_record_payment
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DemoResult"
      security:
        - HTTPBasic: []
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.Demo.SandboxRecordPayment();
                  // TODO: Handle 'response' of type DemoResult
              }
              catch (ApiException<RawError> ex)
              {
                  // TODO: Handle 'ex.Error' of type RawError
              }
        - lang: python
          label: Python
          sources:
            Example: |-
              try:
                  response = client.demo.sandbox_record_payment()
                  # TODO: Handle 'response' of type DemoResult
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type RawError
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.demo.sandboxRecordPayment();
                // TODO: Handle 'response' of type DemoResult
              } catch (err) {
                // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    DemoResult:
      properties:
        ok:
          type: boolean
          description: True on success
        message:
          type: string
          description: What happened, in plain words, for the console toast
      additionalProperties: true
      type: object
      required:
        - ok
        - message
      title: DemoResult
      description: DemoResult object
info:
  title: AegisFleet
  version: 1.0.0
```