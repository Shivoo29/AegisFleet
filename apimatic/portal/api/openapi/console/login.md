# Login (/docs/api/openapi/console/login)

`POST /api/login`

Check a username and password and set a 12-hour session cookie.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/login:
    post:
      tags:
        - console
      summary: Login
      description: Check a username and password and set a 12-hour session cookie.
      operationId: login
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LoginBody"
        required: true
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/Me"
        "401":
          description: "Login required: HTTP Basic or the session cookie"
        "422":
          description: Validation Error
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/HTTPValidationError"
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.ConsoleApi.Login(
                      new LoginRequest { Body = new LoginBody() });
                  // TODO: Handle 'response' of type Me
              }
              catch (ApiException<LoginError> ex)
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
                  response = client.console.login(LoginBody())
                  # TODO: Handle 'response' of type Me
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type LoginErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.login({ body: {} });
                // TODO: Handle 'response' of type Me
              } catch (err) {
                // TODO: Handle 'err' of type Console.LoginError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    LoginBody:
      properties:
        username:
          type: string
          default: ""
          examples:
            - judge
          description: dev or judge
        password:
          type: string
          default: ""
          examples:
            - <judge password>
          description: Console password
      type: object
      title: LoginBody
      description: LoginBody object
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