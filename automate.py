import os
import datetime
from github import Github
from anthropic import Anthropic
import pandas as pd
import io

# 1. Initialize API Clients
github_token = os.environ["MY_GITHUB_TOKEN"]
anthropic_token = os.environ["ANTHROPIC_API_KEY"]

g = Github(github_token)
client = Anthropic(api_key=anthropic_token)

# 2. Configuration (Customized for Rahaf)
REPO_NAME = "ADRES-Design/UX-Reports"
TEXT_REPORT_PATH = "report.txt"
EXCEL_FILE_PATH = "data.xlsx"

def main():
    repo = g.get_repo(REPO_NAME)
    
    # Check current day of the month
    today = datetime.datetime.now().day
    if today < 4:
        print(f"Today is day {today}. Script is configured to only look for data from the 4th onwards. Stopping.")
        return

    # 3. Try to locate the Excel sheet (data.xlsx)
    try:
        excel_contents = repo.get_contents(EXCEL_FILE_PATH)
    except Exception:
        print(f"Day {today}: '{EXCEL_FILE_PATH}' not found. Will try again tomorrow.")
        return

    print(f"Day {today}: New data found! Beginning processing...")

    # 4. Download and convert the Excel file data so Claude can read it cleanly
    excel_bytes = excel_contents.decoded_content
    # Read the excel file using pandas (a data tool)
    df = pd.read_excel(io.BytesIO(excel_bytes))
    # Convert rows/columns into a clean markdown table structure
    clean_table_data = df.to_markdown(index=False)

    # 5. Fetch your baseline report.txt file to update it
    try:
        text_contents = repo.get_contents(TEXT_REPORT_PATH)
        original_report_text = text_contents.decoded_content.decode("utf-8")
        sha_exists = text_contents.sha
    except Exception:
        # If report.txt doesn't exist yet, we start fresh
        original_report_text = "No previous report data."
        sha_exists = None

    # 6. Send everything to Claude
    prompt = f"""You are analyzing a new set of monthly UX research data.
    
Here is the previous report content for context:
{original_report_text}

Here is the new Excel data uploaded for this month:
{clean_table_data}

Please integrate this new data, update the monthly analysis, and return ONLY the final updated text document layout:"""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    updated_text = response.content[0].text

    # 7. Update the report.txt file
    if sha_exists:
        repo.update_file(
            path=TEXT_REPORT_PATH,
            message="Integrated new monthly Excel data",
            content=updated_text,
            sha=sha_exists
        )
    else:
        repo.create_file(
            path=TEXT_REPORT_PATH,
            message="Initial report creation",
            content=updated_text
        )

    # 8. CRITICAL: Delete data.xlsx so the script doesn't run again tomorrow
    repo.delete_file(
        path=EXCEL_FILE_PATH,
        message="Cleanup: Removing processed data.xlsx",
        sha=excel_contents.sha
    )
    
    print("Success! Data integrated into report.txt, and data.xlsx cleared for next month.")

if __name__ == "__main__":
    main()
