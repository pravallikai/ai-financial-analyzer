import os
import requests

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_ai_advice(metrics: dict) -> str:
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is missing. AI advisory cannot run.")

    prompt = f"""
You are a financial analysis assistant.

Using the following computed metrics, generate clear, practical financial insights.
Reference numbers explicitly. Avoid generic advice.

Metrics:
- Total Income: ${metrics['total_income']}
- Total Expenses: ${metrics['total_expenses']}
- Net Savings: ${metrics['net_savings']}
- Savings Rate: {metrics['savings_rate']}%

Provide:
1. A short summary
2. Key observations
3. One or two actionable suggestions

End with:
"This is educational financial guidance, not professional financial advice."
"""

    payload = {
        "model": "meta-llama/llama-3.1-8b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 400
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        OPENROUTER_API_URL,
        headers=headers,
        json=payload,
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter API error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]
