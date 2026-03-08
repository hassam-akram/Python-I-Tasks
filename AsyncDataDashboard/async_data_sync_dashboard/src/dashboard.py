"""
dashboard.py - Main entry point for the Async Data Sync Dashboard

Key Concepts:
  - asyncio.gather() : runs multiple coroutines CONCURRENTLY
    → All three fetches start at the same time
    → Total time ≈ max(2s, 1s, 1.5s) = ~2s  (NOT 2+1+1.5 = 4.5s)
  - asyncio.run()    : starts the event loop and runs the main coroutine
  
Run this file:
    python -m src.dashboard       (from the project root)
"""

import asyncio
import time
from src.data_sources import fetch_sales_data, fetch_inventory_data, fetch_customer_data
from src.merger import merge_data


def print_header():
    """Print the dashboard header."""
    print()
    print("=" * 55)
    print("     ⚡ ASYNC DATA SYNC DASHBOARD ⚡")
    print("=" * 55)
    print()


def print_summary(summary, elapsed):
    """Print the merged summary in a formatted way."""
    print()
    print("-" * 55)
    print("  📊  MERGED DATA SUMMARY")
    print("-" * 55)

    # Sales
    s = summary["sales"]
    print()
    print("  💰 SALES")
    print(f"     Records fetched  : {s['records_count']}")
    print(f"     Total revenue    : ${s['total_revenue']:,}")
    print(f"     Items sold       : {s['total_items_sold']}")

    # Inventory
    inv = summary["inventory"]
    print()
    print("  📦 INVENTORY")
    print(f"     Records fetched  : {inv['records_count']}")
    print(f"     Total in stock   : {inv['total_in_stock']} units")
    print(f"     Warehouses       : {', '.join(inv['warehouses'])}")

    # Customers
    c = summary["customers"]
    print()
    print("  👥 CUSTOMERS")
    print(f"     Total customers  : {c['total_customers']}")
    print(f"     Total orders     : {c['total_orders']}")
    print(f"     Total spent      : ${c['total_spent']:,}")
    print(f"     Avg per customer : ${c['avg_spent_per_customer']:,}")

    # Timing
    print()
    print("-" * 55)
    print(f"  ⏱️  Completed in {elapsed:.2f} seconds")
    print(f"  🚀 (Sequential would take ~4.5s — async saved ~{4.5 - elapsed:.1f}s!)")
    print("=" * 55)
    print()


async def main():
    """Main async function — fetches, merges, and displays data."""
    print_header()
    print("  Fetching data from 3 sources concurrently...\n")

    start = time.time()

    # ── asyncio.gather() runs all three fetches AT THE SAME TIME ──
    sales, inventory, customers = await asyncio.gather(
        fetch_sales_data(),       # takes ~2.0s
        fetch_inventory_data(),   # takes ~1.0s
        fetch_customer_data(),    # takes ~1.5s
    )

    elapsed = time.time() - start

    # ── Merge the results ──
    summary = merge_data(sales, inventory, customers)

    # ── Display the dashboard ──
    print_summary(summary, elapsed)


# ── Entry Point ──
if __name__ == "__main__":
    asyncio.run(main())
