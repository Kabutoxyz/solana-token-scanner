#!/usr/bin/env python3
"""Solana Token Scanner — DexScreener + Holder Analysis."""
import requests, json, sys, time
from datetime import datetime

DEXSCREENER_API = 'https://api.dexscreener.com/latest/dex'

def get_new_tokens(chain='solana', limit=20):
    """Get newest tokens from DexScreener."""
    url = f'{DEXSCREENER_API}/search?q=solana'
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            pairs = resp.json().get('pairs', [])
            # Filter: only SOL pairs, MC $5K-$50K, age >5min
            results = []
            for p in pairs:
                mc = p.get('fdv', 0) or 0
                liq = p.get('liquidity', {}).get('usd', 0) or 0
                age_ms = int(time.time()*1000) - p.get('pairCreatedAt', 0)
                age_min = age_ms / 60000
                
                if (p.get('chainId') == 'solana' and
                    5000 <= mc <= 50000 and
                    liq >= 3000 and
                    age_min >= 5):
                    results.append({
                        'name': p.get('baseToken', {}).get('name', '?'),
                        'symbol': p.get('baseToken', {}).get('symbol', '?'),
                        'address': p.get('baseToken', {}).get('address', ''),
                        'mc': mc,
                        'liquidity': liq,
                        'age_min': round(age_min, 1),
                        'price_usd': p.get('priceUsd', '0'),
                        'volume_24h': p.get('volume', {}).get('h24', 0),
                        'price_change_5m': p.get('priceChange', {}).get('m5', 0),
                        'url': p.get('url', ''),
                    })
            return sorted(results, key=lambda x: x['mc'])
    except Exception as e:
        print(f'Error: {e}')
    return []

def analyze_token(token):
    """Print token analysis."""
    print(f"\n{'='*50}")
    print(f"  {token['symbol']} ({token['name']})")
    print(f"{'='*50}")
    print(f"  MC: ${token['mc']:,.0f}")
    print(f"  Liq: ${token['liquidity']:,.0f}")
    print(f"  Age: {token['age_min']} min")
    print(f"  Price: ${token['price_usd']}")
    print(f"  5m Change: {token.get('price_change_5m', 0):+.1f}%")
    print(f"  Vol 24h: ${token.get('volume_24h', 0):,.0f}")
    print(f"  {token['url']}")

if __name__ == '__main__':
    print(f"🔍 Solana Token Scanner")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Filter: MC $5K-$50K, Liq >$3K, Age >5min\n")
    
    tokens = get_new_tokens()
    if tokens:
        print(f"Found {len(tokens)} tokens:")
        for t in tokens[:10]:
            analyze_token(t)
    else:
        print("No tokens matching filters found.")
