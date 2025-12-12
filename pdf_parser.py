import pandas as pd
import re
from PyPDF2 import PdfReader

REQUIRED_COLUMNS = ["date", "description", "amount", "category"]

AMOUNT_REGEX = re.compile(r"[-+]?\$?\d+(?:,\d{3})*(?:\.\d+)?")

def parse_pdf(file) -> pd.DataFrame:
    """
    Parses a PDF bank statement or expense summary.
    Falls back to text extraction if structured tables are unavailable.
    """

    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    if not text.strip():
        raise ValueError("Unable to extract text from PDF")

    rows = []

    for line in text.splitlines():
        amounts = AMOUNT_REGEX.findall(line)
        if not amounts:
            continue

        amount_str = amounts[-1].replace("$", "").replace(",", "")
        try:
            amount = float(amount_str)
        except ValueError:
            continue

        description = line.replace(amounts[-1], "").strip()

        rows.append({
            "date": "Unknown",
            "description": description if description else "Unknown",
            "amount": amount,
            "category": "Uncategorized"
        })

    if not rows:
        raise ValueError("No financial rows detected in PDF")

    df = pd.DataFrame(rows)
    df = df[REQUIRED_COLUMNS]

    return df
