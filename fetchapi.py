import requests
import os
from dotenv import load_dotenv
import sys

severity_lists = ["low", "medium", "high", "undetermined", "info", "concerns", "enhancement"]

load_dotenv()
access_token = os.getenv("ACCESS_TOKEN")
owner = os.getenv("ORGANIZATION")
#repo = 'audit-tutorial-project'

headers = {
    "Authorization": f"Bearer {access_token}",
    "Accept": "application/vnd.github.v3+json"
}

def get_all_issues(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    response = requests.get(url, headers=headers)
    response_json = response.json()
    issue_list = []

    if response.status_code == 200:
        for res in response_json:
            issue_list.append(res['number'])
     
    return issue_list

def generate_all_files(owner, repo_name):
    repo = f'audit-{repo_name}'
    print(repo)
    issue_list = get_all_issues(owner, repo)
    for issue in issue_list:
        fetch_github_issue(owner, repo, issue)

def fetch_github_issue(owner, repo, issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    response = requests.get(url, headers=headers)
    response_json = response.json()

    if response.status_code == 200:
        issue_title = response_json['title']
        issue_body = response_json['body']
        issue_labels = [label['name'] for label in response_json['labels']]
        count_ok = 0
        is_issue_valid = False

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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        repo_name = sys.argv[1]
        generate_all_files(owner, repo_name)
    else:
        print("No input value provided.")