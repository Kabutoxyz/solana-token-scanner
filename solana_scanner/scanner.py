"""
Scanner — Query Solana blockchain for token data.
"""
import requests
import json
from typing import List, Dict, Optional


class SolanaScanner:
    """Scan Solana tokens via public RPC."""
    
    RPC_URL = "https://api.mainnet-beta.solana.com"
    
    def __init__(self, rpc_url: Optional[str] = None):
        """Initialize scanner with RPC endpoint.
        
        Args:
            rpc_url: Solana RPC URL (default: mainnet-beta).
        """
        self.rpc_url = rpc_url or self.RPC_URL
        self.session = requests.Session()
    
    def _rpc_call(self, method: str, params: list = None) -> Dict:
        """Make a JSON-RPC call to Solana.
        
        Args:
            method: RPC method name.
            params: Method parameters.
        
        Returns:
            RPC response result.
        """
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or [],
        }
        resp = self.session.post(self.rpc_url, json=payload, timeout=30)
        return resp.json().get("result", {})
    
    def get_token_supply(self, mint_address: str) -> Optional[Dict]:
        """Get token supply information.
        
        Args:
            mint_address: SPL token mint address.
        
        Returns:
            Dict with supply amount and decimals.
        """
        result = self._rpc_call("getTokenSupply", [mint_address])
        if not result:
            return None
        
        value = result.get("value", {})
        return {
            "mint": mint_address,
            "amount": int(value.get("amount", 0)),
            "decimals": value.get("decimals", 0),
            "ui_amount": float(value.get("uiAmount", 0)),
        }
    
    def get_token_largest_holders(
        self, mint_address: str, limit: int = 20
    ) -> List[Dict]:
        """Get largest token holders.
        
        Args:
            mint_address: SPL token mint address.
            limit: Number of top holders to return.
        
        Returns:
            List of holder dicts with address and balance.
        """
        result = self._rpc_call("getTokenLargestAccounts", [mint_address])
        if not result:
            return []
        
        accounts = result.get("value", [])[:limit]
        holders = []
        for acc in accounts:
            holders.append({
                "address": acc.get("address", ""),
                "amount": int(acc.get("amount", 0)),
                "decimals": acc.get("decimals", 0),
                "ui_amount": float(acc.get("uiAmount", 0)),
            })
        
        return holders
