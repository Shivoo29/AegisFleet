# Inbox (/docs/api/openapi/console/inbox)

`POST /api/inbox`

Run Sentinel inline (a few seconds) so the console gets the verdict in one call.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/inbox:
    post:
      tags:
        - console
      summary: Inbox
      description: Run Sentinel inline (a few seconds) so the console gets the verdict
        in one call.
      operationId: inbox
      requestBody:
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/InboxEmail"
        required: true
      responses:
        "200":
          description: OK
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/InboxVerdict"
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
                  var response = await client.ConsoleApi.Inbox(
                      new InboxRequest { Body = new InboxEmail() });
                  // TODO: Handle 'response' of type InboxVerdict
              }
              catch (ApiException<InboxError> ex)
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
                  response = client.console.inbox(InboxEmail())
                  # TODO: Handle 'response' of type InboxVerdict
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type InboxErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.inbox({ body: {} });
                // TODO: Handle 'response' of type InboxVerdict
              } catch (err) {
                // TODO: Handle 'err' of type Console.InboxError, discriminated with 'err.payload.kind'
              }
components:
  securitySchemes:
    HTTPBasic:
      type: http
      scheme: basic
  schemas:
    InboxEmail:
      properties:
        subject_id:
          anyOf:
            - type: string
              description: "What this is about: an invoice, dispute or email id"
            - type: "null"
              description: Not set
          examples:
            - INV-0007
          description: "What this is about: an invoice, dispute or email id"
        invoice_id:
          anyOf:
            - type: string
              description: Invoice id, e.g. INV-0007
            - type: "null"
              description: Not set
          examples:
            - INV-0007
          description: Invoice id, e.g. INV-0007
        from:
          anyOf:
            - type: string
              description: Sender address
            - type: "null"
              description: Not set
          examples:
            - service@paypa1-support.com
          description: Sender address
        subject:
          anyOf:
            - type: string
              description: Email subject
            - type: "null"
              description: Not set
          examples:
            - "Payment received: $600.00"
          description: Email subject
        body:
          anyOf:
            - type: string
              description: Email body text
            - type: "null"
              description: Not set
          examples:
            - You have received a payment of $600.00. Ship the order now.
          description: Email body text
      additionalProperties: true
      type: object
      title: InboxEmail
      description: InboxEmail object
    InboxVerdict:
      properties:
        run_id:
          anyOf:
            - type: string
              description: Agent run id
            - type: "null"
              description: Not set
          description: Agent run id
        status:
          anyOf:
            - type: string
              description: Current status
            - type: "null"
              description: Not set
          description: Current status
        verdict:
          anyOf:
            - type: object
              description: "Sentinel verdict: scam | legit | unsure, with red flags"
            - type: "null"
              description: Not set
          description: "Sentinel verdict: scam | legit | unsure, with red flags"
      type: object
      title: InboxVerdict
      description: InboxVerdict object
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