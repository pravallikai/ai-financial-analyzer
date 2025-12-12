def generate_ai_advice(metrics: dict) -> str:
    """
    Generates plain-English financial insights.
    Uses deterministic logic to guarantee free, stable behavior.
    """

    income = metrics.get("total_income", 0)
    expenses = metrics.get("total_expenses", 0)
    savings = metrics.get("net_savings", 0)
    savings_rate = metrics.get("savings_rate", 0)

    lines = []

    lines.append(f"Your total income is ${income:.2f}.")
    lines.append(f"Your total expenses are ${expenses:.2f}.")
    lines.append(f"Your net savings are ${savings:.2f}, resulting in a savings rate of {savings_rate:.2f}%.")

    if savings_rate < 10:
        lines.append("Your savings rate is relatively low. You may want to review discretionary spending categories.")
    elif savings_rate < 20:
        lines.append("Your savings rate is moderate. Increasing savings slightly could improve financial resilience.")
    else:
        lines.append("Your savings rate is strong. You are saving a healthy portion of your income.")

    category_spend = metrics.get("category_spend")
    if category_spend is not None and not category_spend.empty:
        top_category = category_spend.index[0]
        top_amount = category_spend.iloc[0]
        lines.append(
            f"Your highest spending category is '{top_category}', totaling ${top_amount:.2f}."
        )

    anomalies = metrics.get("anomalies")
    if anomalies is not None and not anomalies.empty:
        lines.append(
            "Some transactions appear unusually large compared to your normal spending. Reviewing these may help identify errors or one-time expenses."
        )

    lines.append("")
    lines.append("Disclaimer: This is educational financial guidance, not professional financial advice.")

    return "\n".join(lines)
