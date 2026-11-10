# Post Killswitch (/docs/api/openapi/console/post_killswitch)

`POST /api/killswitch`

Turn the kill switch on or off. While on, the gateway denies every agent action.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/killswitch:
    post:
      tags:
        - console
      summary: Post Killswitch
      description: Turn the kill switch on or off. While on, the gateway denies every
        agent action.
      operationId: post_killswitch
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/KillSwitchBody"
        required: true
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/KillSwitch"
        "401":
          description: "Login required: HTTP Basic or the session cookie"
        "422":
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
      security:
        - HTTPBasic: []
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.ConsoleApi.PostKillswitch(
                      new PostKillswitchRequest
                      {
                          Body = new KillSwitchBody(),
                      });
                  // TODO: Handle 'response' of type KillSwitch
              }
              catch (ApiException<PostKillswitchError> ex)
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
                  response = client.console.post_killswitch(
                      KillSwitchBody()
                  )
                  # TODO: Handle 'response' of type KillSwitch
              except ApiError as e:
                  # TODO: Handle 'e.error' of type PostKillswitchErrorBody
                  ...
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.postKillswitch({
                  body: {},
                });
                // TODO: Handle 'response' of type KillSwitch
              } catch (err) {
                // TODO: Handle 'err' of type Console.PostKillswitchError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    KillSwitchBody:
      properties:
        on:
          type: boolean
          description: true stops every agent action at the gateway
          default: false
      type: object
      title: KillSwitchBody
      description: KillSwitchBody object
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