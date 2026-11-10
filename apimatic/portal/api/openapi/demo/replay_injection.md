# Replay Injection (/docs/api/openapi/demo/replay_injection)

`POST /api/demo/replay_injection`

An email told an agent to refund. Sentinel isn't allowed to refund -> gateway DENY, sealed.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/demo/replay_injection:
    post:
      tags:
        - demo
      summary: Replay Injection
      description: An email told an agent to refund. Sentinel isn't allowed to refund
        -> gateway DENY, sealed.
      operationId: replay_injection
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
                  var response = await client.Demo.ReplayInjection();
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
                  response = client.demo.replay_injection()
                  # TODO: Handle 'response' of type DemoResult
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type RawError
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.demo.replayInjection();
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