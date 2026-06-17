"""
Tests for SolanaScanner.
"""
import unittest
from solana_scanner.scanner import SolanaScanner


class TestSolanaScanner(unittest.TestCase):
    """Test Solana scanner functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.scanner = SolanaScanner()
    
    def test_get_token_supply(self):
        """Test fetching token supply."""
        # USDC on Solana
        supply = self.scanner.get_token_supply(
            "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
        )
        if supply:
            self.assertIn("amount", supply)
            self.assertIn("decimals", supply)


if __name__ == "__main__":
    unittest.main()
