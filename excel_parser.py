import pandas as pd

REQUIRED_COLUMNS = ["date", "description", "amount", "category"]

def parse_excel(file) -> pd.DataFrame:
    """
    Reads an Excel (.xlsx) file, auto-detects the first valid sheet,
    and normalizes it to:
    date | description | amount | category
    """

    xls = pd.ExcelFile(file)
    df = None

    # Find the first sheet with an amount-like column
    for sheet_name in xls.sheet_names:
        temp_df = xls.parse(sheet_name)
        temp_df.columns = [c.strip().lower() for c in temp_df.columns]

        if any("amount" in c or "amt" in c or "value" in c for c in temp_df.columns):
            df = temp_df
            break

    if df is None:
        raise ValueError("No valid sheet with amount column found in Excel file")

    # Normalize column names
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

    # Ensure required columns
    if "date" not in df:
        df["date"] = "Unknown"
    if "description" not in df:
        df["description"] = "Unknown"
    if "category" not in df:
        df["category"] = "Uncategorized"

    if "amount" not in df:
        raise ValueError("Excel file must contain an amount column")

    # Keep only standard schema
    df = df[REQUIRED_COLUMNS]

    # Clean amount
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    return df
