import requests
import base64
import os
from dotenv import load_dotenv

load_dotenv()

# Fetch the access token from the environment
access_token = os.getenv("ACCESS_TOKEN")
organization = os.getenv("ORGANIZATION")
repository = 'report-tutorial-project'
readme_file = "./README.md"

def write_readme_to_github(access_token, organization, repository, readme_file):
    # API endpoint URLs
    base_url = "https://api.github.com"
    readme_url = f"{base_url}/repos/{organization}/{repository}/contents/README.md"

    # Headers for authentication
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Read the content of the README file
    with open(readme_file, "r") as file:
        readme_content = file.read()

    # Create the request payload
    payload = {
        "message": "Update README",
        "content": readme_content
    }

    # Encode the content as Base64
    encoded_content = base64.b64encode(readme_content.encode()).decode()
    payload["content"] = encoded_content

    # Get the current README file SHA
    response = requests.get(readme_url, headers=headers)
    if response.status_code == 200:
        current_readme = response.json()
        payload["sha"] = current_readme["sha"]

    # Create or update the README file
    response = requests.put(readme_url, headers=headers, json=payload)

    if response.status_code == 200:
        print("README file successfully written to GitHub repository.")
    else:
        print("Error occurred while writing README file:", response.status_code)

write_readme_to_github(access_token, organization, repository, readme_file)
