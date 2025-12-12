#when we first try to deploy to Streamlit Community Cloud we use this minimal app to verify deployment works
#it starts with the main app later
#import streamlit as st

#st.set_page_config(page_title="AI Financial Analyzer", layout="wide")
#st.title("AI Financial Analyzer — Smoke Test ✅")
#st.write("If you can see this, Streamlit Community Cloud deployment works.")

#main app will be in app.py
import streamlit as st # Imports the Streamlit library for creating web applications.
import pandas as pd # Imports the Pandas library, typically used for data manipulation and analysis, especially DataFrames.

# --- Import custom parser functions ---
from parsers.csv_parser import parse_csv # Imports the function to read and process CSV files.
from parsers.excel_parser import parse_excel # Imports the function to read and process Excel files.
from parsers.pdf_parser import parse_pdf # Imports the function to read and process PDF files.
from parsers.text_parser import parse_text # Imports the function to read and process free-form text input.

# --- Import custom analysis and LLM functions ---
from analysis.finance_metrics import compute_financial_metrics # Imports the function to calculate key financial figures.
from llm.llm_client import generate_ai_advice # Imports the function to generate advice using a Large Language Model (LLM).

st.set_page_config(page_title="AI Financial Analyzer", layout="wide") # Configures the Streamlit page: sets the browser tab title and uses a wider layout.
st.title("AI Financial Analyzer") # Displays the main title "AI Financial Analyzer" on the web page.

st.write( # Displays a multiline descriptive text block on the web page.
    "Upload financial data (CSV, Excel, PDF) or enter expenses as free text. " # Part of the descriptive text explaining data input options.
    "The system analyzes your data and generates AI-powered financial insights." # Continues the descriptive text explaining the system's purpose.
)

# -------- Input Section --------
st.header("1. Provide Your Data") # Displays a section header for the data input area.

uploaded_file = st.file_uploader( # Creates an object for the file upload widget, storing the uploaded file object.
    "Upload CSV, Excel (.xlsx), or PDF", # Text prompt displayed above the upload widget.
    type=["csv", "xlsx", "pdf"] # Specifies the accepted file extensions for the upload widget.
)

text_input = st.text_area( # Creates an object for the text input area widget, storing the user's entered text.
    "Or enter expenses in text (example: I spent $120 on flight tickets and $80 on hotel.)", # Text prompt displayed above the text area.
    height=120 # Sets the display height of the text area in pixels.
)

df = None # Initializing the variable 'df' (for DataFrame) to hold the parsed financial data, setting it to None.
error = None # Initializing the variable 'error' to capture any parsing exceptions, setting it to None.

try: # Starts a block of code to be tested for errors (exception handling).
    if uploaded_file is not None: # Checks if a file has been successfully uploaded by the user.
        if uploaded_file.name.lower().endswith(".csv"): # Checks if the uploaded file's name ends with ".csv" (case-insensitive).
            df = parse_csv(uploaded_file) # Calls the imported function to process the CSV file, creating the DataFrame 'df'.
        elif uploaded_file.name.lower().endswith(".xlsx"): # Checks if the uploaded file's name ends with ".xlsx" (case-insensitive).
            df = parse_excel(uploaded_file) # Calls the imported function to process the Excel file, creating the DataFrame 'df'.
        elif uploaded_file.name.lower().endswith(".pdf"): # Checks if the uploaded file's name ends with ".pdf" (case-insensitive).
            df = parse_pdf(uploaded_file) # Calls the imported function to process the PDF file, creating the DataFrame 'df'.

    elif text_input.strip(): # Checks if the text input area contains non-whitespace text.
        df = parse_text(text_input) # Calls the imported function to process the free text, creating the DataFrame 'df'.

except Exception as e: # Catches any unexpected error (Exception object 'e') that occurred in the 'try' block.
    error = str(e) # Stores the error message (converted to a string) in the 'error' variable.

if error: # Checks if the 'error' variable contains a message (i.e., an exception occurred).
    st.error(error) # Displays the captured error message as a Streamlit error alert.
    st.stop() # Stops the execution of the Streamlit script, preventing further code from running.

if df is None or df.empty: # Checks if the DataFrame 'df' is still None OR if it's an empty DataFrame.
    st.info("Please upload a file or enter text to begin.") # Displays an informational message to guide the user.
    st.stop() # Stops the execution of the Streamlit script until data is provided.

# -------- Preview --------
st.header("2. Parsed Data Preview") # Displays a section header for the data preview.
st.dataframe(df, use_container_width=True) # Displays the parsed DataFrame 'df' as an interactive table, using the full width.

# -------- Analysis --------
metrics = compute_financial_metrics(df) # Calls the function to calculate financial metrics from the DataFrame 'df', storing the results in the 'metrics' dictionary object.

st.header("3. Financial Summary") # Displays a section header for the financial summary.

col1, col2, col3, col4 = st.columns(4) # Creates four column layout objects for displaying metrics side-by-side.
col1.metric("Total Income", f"${metrics['total_income']}") # Displays the Total Income metric in the first column.
col2.metric("Total Expenses", f"${metrics['total_expenses']}") # Displays the Total Expenses metric in the second column.
col3.metric("Net Savings", f"${metrics['net_savings']}") # Displays the Net Savings metric in the third column.
col4.metric("Savings Rate", f"{metrics['savings_rate']}%") # Displays the Savings Rate metric in the fourth column.

# Category Spend
if metrics["category_spend"] is not None and not metrics["category_spend"].empty: # Checks if category spending data exists and is not empty.
    st.subheader("Category-wise Spending") # Displays a smaller header for the category spending chart.
    st.bar_chart(metrics["category_spend"]) # Displays a bar chart using the category spending data.

# Monthly Trend
if metrics["monthly_trend"] is not None and not metrics["monthly_trend"].empty: # Checks if monthly trend data exists and is not empty.
    st.subheader("Monthly Trend") # Displays a smaller header for the monthly trend chart.
    st.line_chart(metrics["monthly_trend"]) # Displays a line chart using the monthly trend data.

# Anomalies
if metrics["anomalies"] is not None and not metrics["anomalies"].empty: # Checks if anomaly data exists and is not empty.
    st.subheader("Anomalous Transactions") # Displays a smaller header for the anomalous transactions table.
    st.dataframe(metrics["anomalies"], use_container_width=True) # Displays the DataFrame of anomalous transactions.

# -------- AI Advisory --------
st.header("4. AI Financial Advice (NVIDIA LLM)") # Displays a section header for the AI advice feature.

if st.button("Generate AI Advice"): # Creates an object for a button labeled "Generate AI Advice" and checks if it's clicked.
    with st.spinner("Generating AI-powered financial insights..."): # Creates a context manager that displays a spinning loading indicator while code runs.
        advice = generate_ai_advice(metrics) # Calls the function to get financial advice from the LLM, passing the calculated metrics. The output text is stored in 'advice'.
        st.text_area("AI Advice", advice, height=300) # Displays the generated advice text in a non-editable text area.

# -------- Download Report --------
st.header("5. Download Report") # Displays a section header for the report download feature.

report_text = f""" # Starts the creation of a multiline string object using f-string formatting for the downloadable report content.
AI Financial Analyzer Report # Line of text in the report.

Total Income: ${metrics['total_income']} # Inserts the calculated total income into the report text.
Total Expenses: ${metrics['total_expenses']} # Inserts the calculated total expenses into the report text.
Net Savings: ${metrics['net_savings']} # Inserts the calculated net savings into the report text.
Savings Rate: {metrics['savings_rate']}% # Inserts the calculated savings rate into the report text.

Disclaimer: # Line of text in the report.
This is educational financial guidance, not professional financial advice. # Line of text in the report.
""" # Ends the multiline string definition.

st.download_button( # Creates an object for a download button widget.
    label="Download Report (TXT)", # Sets the label text displayed on the button.
    data=report_text, # Provides the 'report_text' string object as the content to be downloaded.
    file_name="financial_report.txt", # Specifies the default filename for the downloaded file.
    mime="text/plain" # Specifies the MIME type of the file (plain text).
)