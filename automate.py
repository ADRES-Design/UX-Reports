import os
from github import Github
from anthropic import Anthropic

# 1. Initialize API Clients using environment secrets
github_token = os.environ["MY_GITHUB_TOKEN"]
anthropic_token = os.environ["ANTHROPIC_API_KEY"]

g = Github(github_token)
client = Anthropic(api_key=anthropic_token)

# 2. Define repository and target file details (Customized for Rahaf)
REPO_NAME = "ADRES-Design/UX-Reports"
FILE_PATH = "report.txt"

def main():
    repo = g.get_repo(REPO_NAME)
    
    # 3. Download the current file content from GitHub
    file_contents = repo.get_contents(FILE_PATH)
    original_text = file_contents.decoded_content.decode("utf-8")
    
    # 4. Send the text to Claude
    prompt = f"Update this text document for the new month. Return ONLY the updated contents:\n\n{original_text}"
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=4000,
        temperature=0.2,
        messages=[{"role": "user", "content": prompt}]
    )
    updated_text = response.content[0].text
    
    # 5. Push the edited file back to GitHub
    repo.update_file(
        path=FILE_PATH,
        message="Monthly recursive update by Claude",
        content=updated_text,
        sha=file_contents.sha  # Unique ID required by GitHub to overwrite the file
    )
    print("File successfully updated!")

if __name__ == "__main__":
    main()
