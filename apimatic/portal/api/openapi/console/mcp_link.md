# Mcp Link (/docs/api/openapi/console/mcp_link)

`GET /api/mcp/link`

A personal MCP URL (token inside, valid 14 days) for any AI client that only accepts a URL.

```yaml
openapi: 3.2.0
servers:
  - url: https://aegisfleet.solvor.co.in
    description: Live demo (PayPal sandbox)
    x-environment: production
paths:
  /api/mcp/link:
    get:
      tags:
        - console
      summary: Mcp Link
      description: A personal MCP URL (token inside, valid 14 days) for any AI client
        that only accepts a URL.
      operationId: mcp_link
      responses:
        "200":
          description: Successful Response
          content:
            application/json:
              schema:
                type: object
                title: Response Mcp Link
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
                  var response = await client.ConsoleApi.McpLink();
                  // TODO: Handle 'response' of type object
              }
              catch (ApiException<McpLinkError> ex)
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
                  response = client.console.mcp_link()
                  # TODO: Handle 'response' of type Any
              except ApiError as e:
                  ...  # TODO: Handle 'e.error' of type McpLinkErrorBody
        - lang: typescript
          label: TypeScript
          sources:
            Example: >-
              try {
                const response = await client.console.mcpLink();
                // TODO: Handle 'response' of type Record<string, unknown>
              } catch (err) {
                // TODO: Handle 'err' of type Console.McpLinkError, discriminated with 'err.payload.kind'
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