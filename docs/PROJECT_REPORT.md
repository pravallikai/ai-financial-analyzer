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

**Context** 
In this project, we designed and implemented a complete AI-Based Personal Finance Analysis and Advisory System from the ground up, using only free and open-source technologies. The entire development process was carried out in Visual Studio Code on a Windows 11 environment, ensuring a reproducible and industry-relevant workflow. We structured the project in a modular way so that each component—data parsing, financial analysis, AI advisory, and web interface—could be developed, tested, and maintained independently. This architectural decision was intentional, as it reflects real-world software engineering practices and supports scalability and future enhancements.

The first major task involved building a robust data ingestion and parsing pipeline. We implemented custom parsers capable of reading financial data from multiple commonly used formats, including CSV, Excel, PDF, and plain text. Using Python libraries such as pandas, the system standardizes all incoming data into a consistent tabular structure with clearly defined fields such as date, description, and transaction amount. This normalization step is critical, as it allows the system to treat heterogeneous input formats uniformly and ensures reliable downstream analysis regardless of how the user provides their financial data.

Once the data was successfully parsed, we developed a Financial Analysis Module responsible for computing meaningful financial metrics. This module calculates total income, total expenses, net savings, category-wise spending distribution, monthly trends, and basic anomaly detection. Special care was taken to convert all analytical outputs into Python-native data types to ensure compatibility with web-based APIs and frontend visualization. Rather than presenting raw numbers alone, the analysis was structured to support interpretability, enabling the system to later explain what the numbers mean, not just what they are.

A core innovation of this project lies in the AI Advisory Module, which transforms numerical financial analysis into human-readable, point-wise financial insights. To ensure the project remained completely free, we deliberately avoided paid APIs and instead used open-source, locally executable Large Language Models from the Hugging Face Transformers ecosystem. Through carefully designed prompts, the AI model was instructed to behave as a financial advisor—producing honest, clear, and actionable advice written in straightforward English. This step demonstrates how generative AI can be applied responsibly and affordably to real-world financial decision support.

Finally, we integrated all components into a web-based application using FastAPI for the backend and HTML, CSS, and JavaScript for the frontend. Users can upload their financial files, trigger analysis, and receive both quantitative reports and AI-generated advisory explanations through an intuitive interface. The completed project was version-controlled using GitHub, making it suitable for portfolio presentation and academic evaluation. Overall, this project serves as a full end-to-end demonstration of how artificial intelligence, data analytics, and software engineering can be combined to deliver an intelligent, user-centric financial advisory system using only free resources.
