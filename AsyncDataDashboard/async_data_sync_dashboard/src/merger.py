"""
merger.py - Merges data from all three sources into a combined summary

Key Concept:
  - Takes raw data from sales, inventory, and customers
  - Computes summary statistics (totals, averages, counts)
  - Returns a single dictionary that the dashboard can display
"""


def merge_data(sales, inventory, customers):
    """
    Merge three datasets into one combined summary dictionary.

    Args:
        sales     : list of sales records
        inventory : list of inventory records  
        customers : list of customer records

    Returns:
        dict with merged summary information
    """

    # ── Sales Summary ──
    total_revenue = sum(item["amount"] * item["qty"] for item in sales)
    total_items_sold = sum(item["qty"] for item in sales)

    # ── Inventory Summary ──
    total_in_stock = sum(item["in_stock"] for item in inventory)
    warehouses = set(item["warehouse"] for item in inventory)

    # ── Customer Summary ──
    total_customers = len(customers)
    total_orders = sum(c["orders"] for c in customers)
    total_spent = sum(c["total_spent"] for c in customers)
    avg_spent = total_spent / total_customers if total_customers else 0

    # ── Combined Summary ──
    summary = {
        "sales": {
            "records_count": len(sales),
            "total_revenue": total_revenue,
            "total_items_sold": total_items_sold,
        },
        "inventory": {
            "records_count": len(inventory),
            "total_in_stock": total_in_stock,
            "warehouses": sorted(warehouses),
        },
        "customers": {
            "total_customers": total_customers,
            "total_orders": total_orders,
            "total_spent": total_spent,
            "avg_spent_per_customer": round(avg_spent, 2),
        },
    }

    return summary
