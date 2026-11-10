# Demo Status (/docs/api/openapi/demo/demo_status)

`GET /api/demo/status`

200 when demo mode is on (404 otherwise).

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/demo/status:
    get:
      tags:
        - demo
      summary: Demo Status
      description: 200 when demo mode is on (404 otherwise).
      operationId: demo_status
      responses:
        "200":
          description: Successful Response
          content:
            application/json:
              schema:
                type: object
                title: Response Demo Status
      security:
        - HTTPBasic: []
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.Demo.DemoStatus();
                  // TODO: Handle 'response' of type object
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
                  response = client.demo.demo_status()
                  # TODO: Handle 'response' of type Any
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type RawError
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.demo.demoStatus();
                // TODO: Handle 'response' of type Record<string, unknown>
              } catch (err) {
                // TODO: Handle 'err' of type ApiError, where 'err.payload' is always the Undeclared arm
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
info:
  title: AegisFleet
  version: 1.0.0
```