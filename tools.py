"""Tools available to the agent.

smolagents ships some tools out of the box (web search, wikipedia).
Custom tools below show how to write your own — decorate a function
with @tool and give it a clear docstring; the LLM reads the docstring
to decide when to call it.
"""

import pandas as pd
from smolagents import tool, DuckDuckGoSearchTool, WikipediaSearchTool

# Built-in tools — zero extra code needed
web_search = DuckDuckGoSearchTool()
wikipedia_lookup = WikipediaSearchTool()

# Cache loaded CSVs so we don't re-read the file on every call
_csv_cache = {}


def _load_csv(file_path: str) -> pd.DataFrame:
    """Internal helper: load a CSV once and cache it."""
    if file_path not in _csv_cache:
        _csv_cache[file_path] = pd.read_csv(file_path)
    return _csv_cache[file_path]


def _truncate(text: str, max_chars: int = 3000) -> str:
    """Internal helper: cap tool output length so a single call can't
    blow up the token budget sent to the LLM on the next step."""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + f"\n... [truncated, {len(text) - max_chars} more characters omitted]"


@tool
def calculator(expression: str) -> str:
    """
    Evaluates a basic math expression safely.

    Args:
        expression: A math expression as a string, e.g. "245 * 89 + 12"

    Returns:
        The result of the calculation as a string.
    """
    allowed_chars = "0123456789+-*/(). "
    if not all(ch in allowed_chars for ch in expression):
        return "Error: only numbers and + - * / ( ) are allowed."
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


@tool
def explore_csv(file_path: str) -> str:
    """
    Loads a CSV file and returns its structure: shape, column names,
    data types, and the first 5 rows. ALWAYS call this first before
    using query_csv or aggregate_csv, so you know the exact column names.

    Args:
        file_path: Path to the CSV file, e.g. "data/sales.csv"

    Returns:
        A text summary of the CSV's structure, or an error message.
    """
    try:
        df = _load_csv(file_path)
        return _truncate(
            f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n"
            f"Columns: {list(df.columns)}\n"
            f"Data types:\n{df.dtypes.to_string()}\n\n"
            f"First 5 rows:\n{df.head().to_string()}"
        )
    except Exception as e:
        return f"Error loading CSV: {e}"


@tool
def query_csv(file_path: str, query: str) -> str:
    """
    Filters a CSV using a pandas query expression and returns matching rows.
    Call explore_csv first to see the exact column names available.

    Args:
        file_path: Path to the CSV file (same one used in explore_csv).
        query: A pandas query expression, e.g. "age > 30 and city == 'Chennai'"

    Returns:
        Up to 20 matching rows as text, or an error message.
    """
    try:
        df = _load_csv(file_path)
        result = df.query(query)
        if result.empty:
            return "No rows matched this query."
        return _truncate(result.head(20).to_string())
    except Exception as e:
        return f"Error running query: {e}"


@tool
def aggregate_csv(file_path: str, group_by: str, agg_column: str, agg_func: str = "mean") -> str:
    """
    Groups a CSV by one column and aggregates another (mean, sum, count, min, max).
    Call explore_csv first to see the exact column names available.

    IMPORTANT: group_by must be a CATEGORICAL column with a small number of
    distinct values (e.g. "department", "country", "experience_level") — NOT a
    unique ID column (e.g. "job_id", "employee_id"), since that produces one
    near-useless row per record instead of a real aggregation.

    Args:
        file_path: Path to the CSV file.
        group_by: A categorical column name to group by, e.g. "department"
        agg_column: Column name to aggregate, e.g. "salary"
        agg_func: One of "mean", "sum", "count", "min", "max"

    Returns:
        Top 20 aggregated groups (sorted descending) as text, or an error message.
    """
    try:
        if agg_func not in ("mean", "sum", "count", "min", "max"):
            return "Error: agg_func must be one of mean, sum, count, min, max"
        df = _load_csv(file_path)

        n_unique = df[group_by].nunique()
        if n_unique > 50:
            return (
                f"Error: '{group_by}' has {n_unique} unique values, which is too many "
                f"to group by meaningfully — it's likely a unique ID column. Pick a "
                f"categorical column instead (check explore_csv output for options)."
            )

        result = df.groupby(group_by)[agg_column].agg(agg_func)
        result = result.sort_values(ascending=False).head(20)
        return _truncate(result.to_string())
    except Exception as e:
        return f"Error: {e}"


# --- Want to add your own tool? Copy this template ---
#
# @tool
# def my_tool(query: str) -> str:
#     """
#     One-line description of what this tool does.
#
#     Args:
#         query: description of this argument.
#
#     Returns:
#         description of what gets returned.
#     """
#     ...
#     return "result"