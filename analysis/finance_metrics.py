import pandas as pd
import numpy as np

def compute_financial_metrics(df: pd.DataFrame) -> dict:
    """
    Computes required financial metrics from normalized data.
    """

    df = df.copy()

    # Ensure amount is numeric
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    income = df[df["amount"] > 0]["amount"].sum()
    expenses = df[df["amount"] < 0]["amount"].sum()
    expenses = abs(expenses)

    net_savings = income - expenses
    savings_rate = (net_savings / income * 100) if income > 0 else 0

    # Category-wise spending
    category_spend = (
        df[df["amount"] < 0]
        .groupby("category")["amount"]
        .sum()
        .abs()
        .sort_values(ascending=False)
    )

    # Monthly trend (safe parsing)
    df["parsed_date"] = pd.to_datetime(df["date"], errors="coerce")
    monthly_trend = (
        df.dropna(subset=["parsed_date"])
        .groupby(df["parsed_date"].dt.to_period("M"))["amount"]
        .sum()
    )

    # Simple anomaly detection using IQR
    q1 = df["amount"].quantile(0.25)
    q3 = df["amount"].quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    anomalies = df[
        (df["amount"] < lower_bound) | (df["amount"] > upper_bound)
    ]

    return {
        "total_income": round(income, 2),
        "total_expenses": round(expenses, 2),
        "net_savings": round(net_savings, 2),
        "savings_rate": round(savings_rate, 2),
        "category_spend": category_spend,
        "monthly_trend": monthly_trend,
        "anomalies": anomalies
    }
