from __future__ import annotations


def calculate_order_price(quantity: int, unit_price: int) -> int:
    """Calculate the total order price."""

    return int(quantity) * int(unit_price)
