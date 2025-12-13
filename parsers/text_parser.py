import pandas as pd
import re

REQUIRED_COLUMNS = ["date", "description", "amount", "category"]

# Captures: "$120 on flight tickets" or "120 for hotel"
PATTERN = re.compile(
    r"(?P<amount>\$?\d+(?:\.\d+)?)\s*(?:on|for)?\s*(?P<desc>[A-Za-z][A-Za-z0-9\s\-\&\/]{1,60})",
    re.IGNORECASE
)

def parse_text(text: str) -> pd.DataFrame:
    """
    Extracts transactions from free text into:
    date | description | amount | category
    date defaults to 'Unknown', category defaults to 'Uncategorized'
    """

    text = (text or "").strip()
    if not text:
        raise ValueError("Text input is empty")

    rows = []
    for match in PATTERN.finditer(text):
        amount_raw = match.group("amount").replace("$", "").strip()
        desc = match.group("desc").strip().rstrip(",. ")

        try:
            amount = float(amount_raw)
        except ValueError:
            continue

        rows.append({
            "date": "Unknown",
            "description": desc if desc else "Unknown",
            "amount": amount,
            "category": "Uncategorized"
        })

    if not rows:
        raise ValueError("No transactions detected in text. Example: 'I spent $20 on coffee.'")

    df = pd.DataFrame(rows)
    df = df[REQUIRED_COLUMNS]
    return df
