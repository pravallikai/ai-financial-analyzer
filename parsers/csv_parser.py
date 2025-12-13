import pandas as pd

REQUIRED_COLUMNS = ["date", "description", "amount", "category"]

def parse_csv(file) -> pd.DataFrame:
    """
    Reads a CSV file-like object and normalizes it to:
    date | description | amount | category
    """

    df = pd.read_csv(file)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Map flexible column names
    column_map = {}

    for col in df.columns:
        if "date" in col:
            column_map[col] = "date"
        elif "desc" in col or "merchant" in col or "detail" in col:
            column_map[col] = "description"
        elif "amount" in col or "amt" in col or "value" in col:
            column_map[col] = "amount"
        elif "category" in col or "type" in col:
            column_map[col] = "category"

    df = df.rename(columns=column_map)

    # Ensure required columns exist
    if "date" not in df:
        df["date"] = "Unknown"
    if "description" not in df:
        df["description"] = "Unknown"
    if "category" not in df:
        df["category"] = "Uncategorized"

    if "amount" not in df:
        raise ValueError("CSV must contain an amount column")

    # Keep only standard schema
    df = df[REQUIRED_COLUMNS]

    # Clean amount
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    return df
