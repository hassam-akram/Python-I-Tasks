"""
data_sources.py - Three async mock data sources

Key Concepts:
  - async def   : declares an asynchronous function (a coroutine)
  - await       : pauses the coroutine until the awaited task completes
  - asyncio.sleep() : simulates a network delay WITHOUT blocking other tasks
  
Each function pretends to call a remote API using the API key from config.
They return mock data as lists of dictionaries.
"""

import asyncio
from src.config import SOURCE1_API_KEY, SOURCE2_API_KEY, SOURCE3_API_KEY


# ─────────────────────────────────────────────
# Source 1: Sales Data  (simulates 2s delay)
# ─────────────────────────────────────────────
async def fetch_sales_data():
    """Fetch mock sales records from Source 1."""
    print(f"  [Source 1] Connecting with key: {SOURCE1_API_KEY[:10]}...")
    await asyncio.sleep(2)  # simulate network delay

    data = [
        {"id": 1, "product": "Laptop",    "amount": 1200, "qty": 5},
        {"id": 2, "product": "Mouse",     "amount": 25,   "qty": 50},
        {"id": 3, "product": "Keyboard",  "amount": 75,   "qty": 30},
        {"id": 4, "product": "Monitor",   "amount": 400,  "qty": 10},
    ]
    print(f"  [Source 1] ✓ Received {len(data)} sales records")
    return data


# ─────────────────────────────────────────────
# Source 2: Inventory Data  (simulates 1s delay)
# ─────────────────────────────────────────────
async def fetch_inventory_data():
    """Fetch mock inventory records from Source 2."""
    print(f"  [Source 2] Connecting with key: {SOURCE2_API_KEY[:10]}...")
    await asyncio.sleep(1)  # simulate network delay

    data = [
        {"id": 1, "product": "Laptop",    "in_stock": 20, "warehouse": "A"},
        {"id": 2, "product": "Mouse",     "in_stock": 150, "warehouse": "B"},
        {"id": 3, "product": "Keyboard",  "in_stock": 80,  "warehouse": "B"},
        {"id": 4, "product": "Monitor",   "in_stock": 35,  "warehouse": "A"},
    ]
    print(f"  [Source 2] ✓ Received {len(data)} inventory records")
    return data


# ─────────────────────────────────────────────
# Source 3: Customer Data  (simulates 1.5s delay)
# ─────────────────────────────────────────────
async def fetch_customer_data():
    """Fetch mock customer records from Source 3."""
    print(f"  [Source 3] Connecting with key: {SOURCE3_API_KEY[:10]}...")
    await asyncio.sleep(1.5)  # simulate network delay

    data = [
        {"id": 1, "name": "Alice",   "orders": 3, "total_spent": 1500},
        {"id": 2, "name": "Bob",     "orders": 7, "total_spent": 3200},
        {"id": 3, "name": "Charlie", "orders": 2, "total_spent": 800},
        {"id": 4, "name": "Diana",   "orders": 5, "total_spent": 2100},
        {"id": 5, "name": "Eve",     "orders": 1, "total_spent": 450},
    ]
    print(f"  [Source 3] ✓ Received {len(data)} customer records")
    return data
