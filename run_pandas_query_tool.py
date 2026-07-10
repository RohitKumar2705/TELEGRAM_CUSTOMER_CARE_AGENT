from __future__ import annotations

from typing import Any


def run_pandas_query_tool(df: Any, query: str, use_head: bool = False) -> str:
    """Run a pandas query expression against a DataFrame.

    This is a lightweight local implementation so the project can import and run.
    """

    try:
        target_df = df.head() if use_head else df
        result = target_df.query(query)
        return result.to_json(orient="records")
    except Exception as exc:
        return f"Query execution failed: {exc}"
