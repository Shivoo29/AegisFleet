# Overdue (/docs/api/openapi/demo/overdue)

`POST /api/demo/overdue`

INV-0006 slips 9 days past due -> Collector scores it and sends a capped, polite reminder.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/demo/overdue:
    post:
      tags:
        - demo
      summary: Overdue
      description: INV-0006 slips 9 days past due -> Collector scores it and sends a
        capped, polite reminder.
      operationId: overdue
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
                  var response = await client.Demo.Overdue();
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
                  response = client.demo.overdue()
                  # TODO: Handle 'response' of type DemoResult
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type RawError
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.demo.overdue();
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