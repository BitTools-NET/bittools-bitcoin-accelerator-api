#!/usr/bin/env python3
"""Server-side BitTools API examples; Python 3.9+, standard library only."""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def build_request(command, ids='bitcoin', fiat='usd', txid=None):
    base = os.environ.get('BITTOOLS_API_BASE', 'https://www.bittools.net/api/v1').rstrip('/')
    parsed = urllib.parse.urlsplit(base)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError('BITTOOLS_API_BASE must be an HTTPS API base URL without credentials or query parameters.')
    key = os.environ.get('BITTOOLS_API_KEY', '').strip()
    if not key or '\r' in key or '\n' in key:
        raise ValueError('Set a valid BITTOOLS_API_KEY in the server environment.')
    headers = {'Authorization': 'Bearer ' + key, 'Accept': 'application/json'}
    if command == 'accelerate':
        if not txid or not re.fullmatch(r'[a-fA-F0-9]{64}', txid):
            raise ValueError('TXID must contain exactly 64 hexadecimal characters.')
        headers['Content-Type'] = 'application/json'
        return urllib.request.Request(base + '/accelerator', data=json.dumps({'txid': txid.lower()}).encode(), headers=headers, method='POST')
    coins = ids.split(',')
    if not 1 <= len(coins) <= 100 or any(not re.fullmatch(r'[a-z0-9][a-z0-9-]*', coin) for coin in coins):
        raise ValueError('Use up to 100 comma-separated coin identifiers, such as bitcoin,ethereum.')
    if not re.fullmatch(r'[a-zA-Z]{3,5}', fiat):
        raise ValueError('Use an enabled fiat code such as USD.')
    query = urllib.parse.urlencode({'ids': ids, 'fiat': fiat.upper()})
    return urllib.request.Request(base + '/prices?' + query, headers=headers, method='GET')


def main():
    parser = argparse.ArgumentParser(description='BitTools Bitcoin accelerator and market API examples')
    sub = parser.add_subparsers(dest='command', required=True)
    prices = sub.add_parser('prices', help='Read market prices')
    prices.add_argument('--ids', default='bitcoin')
    prices.add_argument('--fiat', default='usd')
    accelerate = sub.add_parser('accelerate', help='Submit a TXID with approved partner access')
    accelerate.add_argument('txid')
    args = parser.parse_args()
    try:
        request = build_request(args.command, getattr(args, 'ids', 'bitcoin'), getattr(args, 'fiat', 'usd'), getattr(args, 'txid', None))
        with urllib.request.build_opener(NoRedirect()).open(request, timeout=15) as response:
            result = json.load(response)
        if not isinstance(result, dict) or result.get('success') is not True:
            raise ValueError('The API did not return a successful response.')
        print(json.dumps(result, indent=2))
        return 0
    except urllib.error.HTTPError as exc:
        print('API returned HTTP {}. Check permissions, quotas and service availability.'.format(exc.code), file=sys.stderr)
        if exc.code == 429 and exc.headers.get('Retry-After'):
            print('Retry-After: ' + exc.headers['Retry-After'], file=sys.stderr)
        return 1
    except (ValueError, urllib.error.URLError, TimeoutError) as exc:
        print('Request failed: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
