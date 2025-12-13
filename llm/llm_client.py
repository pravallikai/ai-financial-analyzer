import os
import requests
import json

# NVIDIA Chat Completions endpoint
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"


def generate_ai_advice(metrics: dict) -> str:
    """
    Generate AI-powered financial advice using NVIDIA LLM.
    """

    api_key = os.getenv("NVIDIA_API_KEY")

    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY is missing. AI advisory cannot run.")

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
        "model": "meta/llama3-70b-instruct",
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
        NVIDIA_API_URL,
        headers=headers,
        data=json.dumps(payload),
        timeout=30
    )

    if response.status_code != 200:
        raise RuntimeError(f"NVIDIA API error: {response.text}")

    return response.json()["choices"][0]["message"]["content"]
