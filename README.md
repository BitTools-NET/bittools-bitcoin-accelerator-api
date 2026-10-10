# BitTools Bitcoin Transaction Accelerator API

Developer documentation and server-side examples for the [BitTools Bitcoin transaction accelerator](https://www.bittools.net/). Integrate BTC transaction submission for approved partners, retrieve cryptocurrency prices, and build Bitcoin tools with the BitTools API.

[Use the BTC accelerator](https://www.bittools.net/) · [API documentation](https://www.bittools.net/api) · [Partner enquiries](mailto:support@bittools.net)

## Accelerate a stuck Bitcoin transaction

BitTools helps users submit stuck or unconfirmed BTC transactions for acceleration. The website offers a free acceleration option and paid priority options where available. Enter your transaction ID (TXID) on the website to see the options for your transaction.

For wallets, exchanges and other services that need a Bitcoin accelerator integration, API access is arranged directly with BitTools. Accelerator permission must be enabled for your partner key before transaction submission can be used.

This repository contains integration examples and a reference specification. The service runs on BitTools; the private accelerator infrastructure and payment system are not included.

## Repository guide

| File | Purpose |
| --- | --- |
| [Python client](examples/bittools.py) | Fetch prices or submit a TXID with input validation, timeouts and HTTP error handling |
| [PHP example](examples/prices.php) | Fetch prices using PHP 7.4+ and cURL |
| [Integration guide](docs/integration.md) | Authentication, request formats and response handling |
| [OpenAPI specification](openapi.json) | API reference for developer tools |

## Quick start

Clone this repository and open its directory:

```bash
git clone https://github.com/BitTools-NET/bittools-bitcoin-accelerator-api.git
cd bittools-bitcoin-accelerator-api
```

Set `BITTOOLS_API_KEY` in your server environment using your approved BitTools key. Keep it out of source control and browser JavaScript. The examples use `https://www.bittools.net/api/v1` by default.

### Python: Bitcoin price data

Requires Python 3.9+; no third-party packages are needed.

```bash
python3 examples/bittools.py prices --ids bitcoin --fiat usd
```

### PHP: cryptocurrency prices

Requires PHP 7.4+ with the cURL extension.

```bash
php examples/prices.php
```

### Submit a BTC transaction for acceleration

After accelerator access has been enabled for your partner key, replace the placeholder with the public 64-character hexadecimal TXID:

```bash
python3 examples/bittools.py accelerate YOUR_64_CHARACTER_TXID
```

The client sends one POST request and does not automatically retry transaction submissions. If a timeout leaves the outcome unclear, check with BitTools before submitting the same transaction again. See the [integration guide](docs/integration.md) for request and response details.

## Partner integration workflow

1. Contact [support@bittools.net](mailto:support@bittools.net) with your service name and intended API use.
2. Confirm access, available features and limits with our team.
3. Store the issued key on your server and connect your application using the examples.
4. Validate each TXID and handle submission errors separately from confirmation status.

For an approved private test deployment, `BITTOOLS_API_BASE` can override the HTTPS API base URL. Availability and permissions depend on your key. The [live API documentation](https://www.bittools.net/api) takes precedence if the service changes.

## Bitcoin transaction accelerator FAQ

### What is a Bitcoin transaction accelerator?

A Bitcoin transaction accelerator is a service used to help a pending BTC transaction progress toward confirmation. The available approach depends on the transaction and service option. BitTools provides a web interface and partner API access for its acceleration service.

### Can I use BitTools without an API integration?

Yes. Open the [BitTools BTC accelerator](https://www.bittools.net/), enter your TXID and review the available acceleration options. The API is intended for approved partner applications.

### Do I need to provide wallet access?

No. Transaction submission uses a public TXID. BitTools does not need your wallet seed phrase, private keys or wallet password.

### Does an accepted API request mean the transaction is confirmed?

No. Acceptance reports submission to the service. Confirmation is a separate blockchain event, and miners decide which valid transactions enter a block. Timing depends on the transaction, network conditions and selected option.

### Is the accelerator API available to every API key?

No. Accelerator access is limited to approved partnerships and must be enabled for the key. Contact our team before building a production submission flow.

## Support and contributions

For API access, transaction assistance or billing questions, email [support@bittools.net](mailto:support@bittools.net). Use GitHub Issues for bugs in these examples, with reproduction steps and a redacted error message. Never post API keys, wallet credentials or private account details.
