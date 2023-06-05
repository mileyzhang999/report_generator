import requests
import os
from dotenv import load_dotenv
import sys

severity_lists = ["low", "medium", "high", "undetermined", "info", "concerns", "enhancement"]

load_dotenv()
access_token = os.getenv("ACCESS_TOKEN")
owner = os.getenv("ORGANIZATION")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.github.v3+json"
}

base_url = f"https://api.github.com/repos/{owner}"

def get_all_issues(repo):
    url = f"{base_url}/{repo}/issues"
    response = requests.get(url, headers=headers)
    response_json = response.json()
    issue_list = []

    if response.status_code == 200:
        for res in response_json:
            issue_list.append(res['number'])
     
    return issue_list

def generate_all_files(repo):
    issue_list = get_all_issues(repo)
    for issue in issue_list:
        fetch_github_issue(repo, issue)

def fetch_github_issue(repo, issue_number):
    url = f"{base_url}/{repo}/issues/{issue_number}"
    response = requests.get(url, headers=headers)
    response_json = response.json()

    if response.status_code == 200:
        issue_title = response_json['title']
        issue_body = response_json['body']
        issue_labels = [label['name'] for label in response_json['labels']]

        for label in issue_labels:
            if label == "invalid":
                return None

        generate_severity_issue_file(issue_number, issue_body, issue_labels)

        return issue_title
    
    return None

def generate_severity_issue_file(issue_number, issue_body, issue_labels):
    severity = [label for label in issue_labels if label in severity_lists][0]
    file_name = f"{issue_number}-finding-{severity}.md"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(issue_body)
    print(f"Content written to {file_name}")

def fetch_all_md_files(repo):
    files_url = f"{base_url}/{repo}/contents"
    response = requests.get(files_url, headers=headers)
    files = response.json()
    table_list = []

    fetch_images(files)
    md_files = [file for file in files if file['name'].endswith('.md')]

    for file in md_files:
        content_url = file['download_url']
        response = requests.get(content_url, headers=headers)
        content = response.text
        if(is_file_empty(content)):
            continue

        # Write content to a local file
        table_list.append(file['name'])
        file_name = 'OtherMarkDown/' + file['name']
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Downloaded: {file_name}")
    generate_table_contents(table_list)


def fetch_images(contents):
    for content in contents:
        if content["type"] == "file" and content["name"].lower().endswith((".jpg", ".jpeg", ".png", ".gif")):
            download_url = content["download_url"]
            image_data = requests.get(download_url).content

            # Save the image to a file
            image_name = content["name"]
            with open(image_name, "wb") as file:
                file.write(image_data)
            print(f"Downloaded: {image_name}")

def is_file_empty(file):
    content = file.strip()
    return len(content) == 0 or all(char in [' ', '\n'] for char in content)

def fetch_all_default_files():
    files_url = f"{base_url}/default-markdown/contents"
    response = requests.get(files_url, headers=headers)
    files = response.json()

    md_files = [file for file in files if file['name'].endswith('.md')]

    for file in md_files:
        content_url = file['download_url']
        response = requests.get(content_url, headers=headers)
        content = response.text
        if(content == ""):
            continue
        
        # Write content to a local file
        file_name = 'DefaultMarkDown/' + file['name']
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Downloaded: {file_name}")
    

def generate_table_contents(lists):
    content = """
## Table of Contents

- [About Canary Technologies](#about-canary-technologies)
"""
    
    content += '- [Service Scope](#service-scope)\n' if 'service-scope.md' in lists else ''

    content += '- [Project Summary](#project-summary)\n' if 'project-summary.md' in lists else ''

    content += '- [Findings & Improvement Suggestions](#findings--improvement-suggestions)\n'

    content += '- [Use Case Scenarios](#use-case-scenarios)\n' if 'use-case-scenarios.md' in lists else ''

    content += '- [Access Control Analysis](#access-control-analysis)\n' if 'access-control-analysis.md' in lists else ''

    content += '''- [Appendix I: Security Issue Severities](#appendix-i-security-issue-severities)
- [Appendix II: Status Categories](#appendix-ii-status-categories)
- [Disclaimer](#disclaimer)
    \n\n
    '''
    with open('table-content.md', 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Generated: table-content.md")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        repo_name = sys.argv[1]
        repo = f'audit-{repo_name}'
        generate_all_files(repo)
        fetch_all_md_files(repo)
        fetch_all_default_files()
    else:
        print("No input value provided.")