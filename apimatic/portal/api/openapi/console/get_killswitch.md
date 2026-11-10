# Get Killswitch (/docs/api/openapi/console/get_killswitch)

`GET /api/killswitch`

Is the kill switch on?

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/killswitch:
    get:
      tags:
        - console
      summary: Get Killswitch
      description: Is the kill switch on?
      operationId: get_killswitch
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/KillSwitch"
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
                  var response = await client.ConsoleApi.GetKillswitch();
                  // TODO: Handle 'response' of type KillSwitch
              }
              catch (ApiException<GetKillswitchError> ex)
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
                  response = client.console.get_killswitch()
                  # TODO: Handle 'response' of type KillSwitch
              except ApiError as e:
                  # TODO: Handle 'e.error' of type GetKillswitchErrorBody
                  ...
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.getKillswitch();
                // TODO: Handle 'response' of type KillSwitch
              } catch (err) {
                // TODO: Handle 'err' of type Console.GetKillswitchError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    KillSwitch:
      properties:
        on:
          type: boolean
          description: True when the kill switch is on
      type: object
      required:
        - on
      title: KillSwitch
      description: KillSwitch object
info:
  title: AegisFleet
  version: 1.0.0
```