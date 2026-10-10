# BitTools Bitcoin Transaction Accelerator Integration

Connect your server to the BitTools API using the examples in this repository. Base URL: `https://www.bittools.net/api/v1`. Accelerator submission requires approved partner access; contact [support@bittools.net](mailto:support@bittools.net) to discuss your integration.

## Authentication

Send `Authorization: Bearer YOUR_API_KEY` over HTTPS. The key must be active and authorized for the requested feature. Request quotas depend on your key; handle HTTP 429 and read response headers rather than assuming a universal limit.

## Market prices

`GET /prices?ids=bitcoin&fiat=USD`

The API returns JSON. Check the HTTP status and `success` field before reading `data`. Cache successful read responses according to your application needs.

## Bitcoin transaction accelerator submission

`POST /accelerator` with `Content-Type: application/json`:

```json
{"txid":"YOUR_64_CHARACTER_BITCOIN_TRANSACTION_ID"}
```

Replace the placeholder with an actual 64-character hexadecimal TXID. The endpoint requires approved partner access, service availability and accelerator permission on your key. Do not send wallet seed phrases or private keys.

A successful submission uses HTTP 202 and a response containing:

```json
{"success":true,"data":{"txid":"YOUR_TXID","status":"submitted"}}
```

Additional metadata may be present. Submission is distinct from on-chain confirmation. A separate transaction-status endpoint is not included in this API reference.

## Failure handling

| HTTP | Action |
| --- | --- |
| 400 | Correct the request body or TXID. |
| 401 | Check your API key. |
| 403 | Check feature permissions and access availability. |
| 404 | Check the requested asset or endpoint. |
| 429 | Honor `Retry-After` when supplied. |
| 503 | Contact support or retry a read later. Do not blindly repeat submissions. |

A timeout does not prove that a submission failed. Confirm the outcome with BitTools before repeating a POST request. The example clients deliberately avoid automatic transaction retries.

## Production checklist

- Keep the key in a server environment variable, outside source control.
- Retain TLS certificate verification and set request timeouts.
- Validate TXIDs before submission.
- Cache read requests and handle rate limits.
- Redact credentials and private account details from logs and support reports.

See the [live API documentation](https://www.bittools.net/api) for current availability and the [README](../README.md) for quick-start commands.
