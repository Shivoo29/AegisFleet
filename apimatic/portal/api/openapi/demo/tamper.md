# Tamper (/docs/api/openapi/demo/tamper)

`POST /api/demo/tamper`

Edit one sealed entry behind the ledger's back -> verify() points at it.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/demo/tamper:
    post:
      tags:
        - demo
      summary: Tamper
      description: Edit one sealed entry behind the ledger's back -> verify() points at it.
      operationId: tamper
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
                  var response = await client.Demo.Tamper();
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
                  response = client.demo.tamper()
                  # TODO: Handle 'response' of type DemoResult
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type RawError
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.demo.tamper();
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