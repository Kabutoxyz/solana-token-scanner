# solana-token-scanner

Scan Solana SPL tokens for metadata, holders, and transfer history.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Scan a token
solana-scanner scan TOKEN_MINT_ADDRESS

# Get token holders
solana-scanner holders TOKEN_MINT_ADDRESS --limit 20

# Get transfer history
solana-scanner transfers TOKEN_MINT_ADDRESS --limit 50
```

## Features

- Token metadata lookup
- Holder analysis
- Transfer history
- Rich terminal output

## License

MIT
