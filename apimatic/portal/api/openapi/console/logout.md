# Logout (/docs/api/openapi/console/logout)

`POST /api/logout`

Clear the session cookie.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/logout:
    post:
      tags:
        - console
      summary: Logout
      description: Clear the session cookie.
      operationId: logout
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Ok"
        "401":
          description: "Login required: HTTP Basic or the session cookie"
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.ConsoleApi.Logout();
                  // TODO: Handle 'response' of type Ok
              }
              catch (ApiException<LogoutError> ex)
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
                  response = client.console.logout()
                  # TODO: Handle 'response' of type Ok
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type LogoutErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.logout();
                // TODO: Handle 'response' of type Ok
              } catch (err) {
                // TODO: Handle 'err' of type Console.LogoutError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    Ok:
      properties:
        ok:
          type: boolean
          description: True on success
      type: object
      required:
        - ok
      title: Ok
      description: Ok object
info:
  title: AegisFleet
  version: 1.0.0
```