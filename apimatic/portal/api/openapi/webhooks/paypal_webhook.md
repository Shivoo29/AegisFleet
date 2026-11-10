# Paypal Webhook (/docs/api/openapi/webhooks/paypal_webhook)

`POST /webhooks/paypal`

PayPal calls this. The signature is verified with PayPal before the event is sealed and routed.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /webhooks/paypal:
    post:
      tags:
        - webhooks
      summary: Paypal Webhook
      description: PayPal calls this. The signature is verified with PayPal before the
        event is sealed and routed.
      operationId: paypal_webhook
      responses:
        "200":
          description: Successful Response
          content:
            application/json:
              schema:
                type: object
                title: Response Paypal Webhook
      x-apimatic-codeSamples:
        - lang: csharp
          label: C#
          sources:
            Example: |-
              try
              {
                  var response = await client.WebhooksApi.PaypalWebhook();
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
                  response = client.webhooks.paypal_webhook()
                  # TODO: Handle 'response' of type Any
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type RawError
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.webhooks.paypalWebhook();
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