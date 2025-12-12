# AI Financial Analyzer — Project Report

## Abstract
This project presents an AI Financial Analyzer that ingests financial data from multiple formats
(CSV, Excel, PDF, and free text), normalizes it into a unified schema, computes key financial
metrics, and generates natural-language financial insights using a large language model hosted
via NVIDIA’s API. The system is fully deployed on Streamlit Community Cloud using only free
resources.

## Problem Statement
Individuals often store financial information in heterogeneous formats such as spreadsheets,
bank statements, and informal text notes. Manually consolidating and analyzing this data is
time-consuming and error-prone. This project aims to automate data ingestion, financial analysis,
and insight generation in a single, accessible web application.

## System Architecture
The system follows a modular pipeline architecture:
1. Data ingestion and parsing (CSV, Excel, PDF, Text)
2. Schema normalization
3. Financial analytics engine
4. AI advisory layer powered by an NVIDIA-hosted LLM
5. Streamlit-based user interface and visualization layer

## Data Ingestion Methods
- **CSV Parser**: Reads transaction-style CSV files with flexible column naming.
- **Excel Parser**: Automatically detects the first valid worksheet containing financial data.
- **PDF Parser**: Extracts readable text from bank statements and identifies monetary values.
- **Text Parser**: Converts user-typed expense descriptions into structured transactions.

All inputs are normalized to the schema:
`date | description | amount | category`.

## Analytics Performed
The system computes:
- Total income
- Total expenses
- Net savings
- Savings rate
- Category-wise spending
- Monthly spending trends
- Anomaly detection using the Interquartile Range (IQR) method

## AI Advisory Approach
Computed financial metrics are provided as structured context to an NVIDIA-hosted large language
model. The model generates plain-English financial insights that reference actual computed values.
This approach ensures explanations are data-driven rather than generic.

**Disclaimer:** This is educational financial guidance, not professional financial advice.

## Limitations
- PDF parsing accuracy depends on document text quality.
- The system assumes numerical sign conventions for income and expenses.
- AI-generated insights are dependent on LLM availability and response quality.

## Future Improvements
- Improved transaction categorization using machine learning
- Multi-currency support
- Historical budgeting and forecasting
- Enhanced PDF table extraction
