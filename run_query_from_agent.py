from __future__ import annotations

from typing import Any

from modules.tools.run_pandas_query_tool import run_pandas_query_tool


def run_query_from_agent(df: Any, query: str, use_head: bool = False) -> str:
    return run_pandas_query_tool(df=df, query=query, use_head=use_head)
