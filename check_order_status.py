from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Any, Iterable


def _normalize(value: Any) -> str:
    return str(value).strip().lower()


def _candidate_paths() -> Iterable[Path]:
    env_path = os.getenv("ORDER_STATUS_DATA_PATH")
    if env_path:
        yield Path(env_path)

    base_dir = Path(__file__).resolve().parents[2]
    yield base_dir / "orders.csv"
    yield base_dir / "data" / "orders.csv"


def _find_row(order_id: str, customer_name: str, phone_number: str) -> dict[str, str] | None:
    for path in _candidate_paths():
        if not path.exists():
            continue

        with path.open(newline="", encoding="utf-8-sig") as file_handle:
            reader = csv.DictReader(file_handle)
            for row in reader:
                row_order_id = _normalize(row.get("Order ID") or row.get("order_id"))
                row_customer_name = _normalize(row.get("Customer Name") or row.get("customer_name"))
                row_phone_number = _normalize(row.get("Phone Number") or row.get("phone_number"))

                if (
                    row_order_id == _normalize(order_id)
                    and row_customer_name == _normalize(customer_name)
                    and row_phone_number == _normalize(phone_number)
                ):
                    return row

    return None


def check_order_status(order_id: str, customer_name: str, phone_number: str) -> str:
    """Look up an order by the three identity fields.

    The tool checks a CSV file if one is configured through ORDER_STATUS_DATA_PATH
    or available at orders.csv / data/orders.csv in the workspace root.
    """

    row = _find_row(order_id, customer_name, phone_number)
    if row is None:
        return (
            "No matching order was found. "
            "Make sure the Order ID, full name, and phone number are correct."
        )

    return (
        f"Order ID: {row.get('Order ID') or row.get('order_id') or order_id}\n"
        f"Customer Name: {row.get('Customer Name') or row.get('customer_name') or customer_name}\n"
        f"Phone Number: {row.get('Phone Number') or row.get('phone_number') or phone_number}\n"
        f"Delivery Status: {row.get('Delivery Status') or row.get('delivery_status') or 'N/A'}\n"
        f"Order Status: {row.get('Order Status') or row.get('order_status') or 'N/A'}\n"
        f"Order Date: {row.get('Order Date') or row.get('order_date') or 'N/A'}\n"
        f"Quantity: {row.get('Quantity') or row.get('quantity') or 'N/A'}\n"
        f"Total Price (PKR): {row.get('Total Price (PKR)') or row.get('total_price') or 'N/A'}\n"
        f"City: {row.get('City') or row.get('city') or 'N/A'}\n"
        f"Order Tracking Link: {row.get('Order Tracking Link') or row.get('tracking_link') or 'N/A'}"
    )
