from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


DEFAULT_PRODUCT_ROWS = [
    {
        "Product ID": "PRF001",
        "Perfume Name": "Noor Mist",
        "Fragrance Notes": "Fresh floral",
        "Type": "Eau de Parfum",
        "Volume (ml)": 50,
        "Price (PKR)": 3500,
        "Stock": 12,
        "Gender": "Women",
        "Alcohol-Free": "No",
        "Collection": "Luxury Oud",
        "Scent Strength": "Medium",
        "Rating": 4.5,
    },
    {
        "Product ID": "PRF002",
        "Perfume Name": "Rihla Oud",
        "Fragrance Notes": "Warm oud and spice",
        "Type": "Eau de Parfum",
        "Volume (ml)": 100,
        "Price (PKR)": 4900,
        "Stock": 8,
        "Gender": "Unisex",
        "Alcohol-Free": "Yes",
        "Collection": "Luxury Oud",
        "Scent Strength": "Strong",
        "Rating": 4.7,
    },
]


@dataclass
class DummySheetsClient:
    source: str = "local"


def initialize_google_sheets(config: Any):
    """Return a client placeholder and a product DataFrame.

    If a CSV exists at the path in GOOGLE_SHEETS_CSV or data/products.csv,
    it is loaded instead of the built-in sample rows.
    """

    csv_path_value = getattr(config, "PRODUCTS_CSV_PATH", "") or ""
    if csv_path_value:
        csv_path = Path(csv_path_value)
        if csv_path.exists() and csv_path.is_file():
            df = pd.read_csv(csv_path)
            return DummySheetsClient(source=str(csv_path)), df

    env_csv = Path(Path.cwd(), "data", "products.csv")
    if env_csv.exists() and env_csv.is_file():
        df = pd.read_csv(env_csv)
        return DummySheetsClient(source=str(env_csv)), df

    df = pd.DataFrame(DEFAULT_PRODUCT_ROWS)
    return DummySheetsClient(), df
