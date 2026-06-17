#!/usr/bin/env python3
"""
CLI — Command-line interface for Solana token scanning.
"""
import json
import click
from rich.console import Console
from rich.table import Table
from .scanner import SolanaScanner

console = Console()


@click.group()
def main():
    """Scan Solana SPL tokens."""
    pass


@main.command()
@click.argument("mint_address")
@click.option("--rpc", "-r", help="Custom RPC endpoint")
def scan(mint_address, rpc):
    """Scan a token for metadata."""
    scanner = SolanaScanner(rpc_url=rpc)
    supply = scanner.get_token_supply(mint_address)
    
    if not supply:
        console.print(f"[red]Could not fetch token data for {mint_address}[/red]")
        return
    
    table = Table(title=f"🪙 Token: {mint_address[:16]}...", show_lines=True)
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Mint", supply["mint"])
    table.add_row("Total Supply", f"{supply['ui_amount']:,.{supply['decimals']}f}")
    table.add_row("Decimals", str(supply["decimals"]))
    
    console.print(table)


@main.command()
@click.argument("mint_address")
@click.option("--limit", "-l", default=20, help="Number of holders")
def holders(mint_address, limit):
    """Get largest token holders."""
    scanner = SolanaScanner()
    top_holders = scanner.get_token_largest_holders(mint_address, limit=limit)
    
    if not top_holders:
        console.print("[yellow]No holder data found.[/yellow]")
        return
    
    table = Table(title="👥 Top Holders", show_lines=True)
    table.add_column("#", style="dim", justify="right")
    table.add_column("Address", style="cyan")
    table.add_column("Balance", justify="right", style="green")
    
    for i, h in enumerate(top_holders, 1):
        table.add_row(
            str(i),
            h["address"][:16] + "...",
            f"{h['ui_amount']:,.{h['decimals']}f}",
        )
    
    console.print(table)


if __name__ == "__main__":
    main()
