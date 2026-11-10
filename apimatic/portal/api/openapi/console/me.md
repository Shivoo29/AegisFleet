# Me (/docs/api/openapi/console/me)

`GET /api/me`

Who is logged in, and whether they are the seller (dev) or a read-mostly judge.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/me:
    get:
      tags:
        - console
      summary: Me
      description: Who is logged in, and whether they are the seller (dev) or a
        read-mostly judge.
      operationId: me
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Me"
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
                  var response = await client.ConsoleApi.Me();
                  // TODO: Handle 'response' of type Me
              }
              catch (ApiException<MeError> ex)
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
                  response = client.console.me()
                  # TODO: Handle 'response' of type Me
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type MeErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.me();
                // TODO: Handle 'response' of type Me
              } catch (err) {
                // TODO: Handle 'err' of type Console.MeError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    Me:
      properties:
        user:
          type: string
          description: Logged-in user name
        role:
          type: string
          enum:
            - dev
            - judge
          description: dev (seller) or judge
      type: object
      required:
        - user
        - role
      title: Me
      description: Me object
info:
  title: AegisFleet
  version: 1.0.0
```