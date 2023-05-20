import re
import os

def extract_content(former_text, latter_text, text):
    pattern = r"\[" + former_text + "\]\s+(.*?)\s+\[" + latter_text + "\]"
    if latter_text == 'EOF':
        pattern = r"\[" + former_text + "\](.+)(?=EOF)"
    match = re.search(pattern, text, re.DOTALL)
    
    if match:
        content = match.group(1)
        return content.strip()
    
    return 'N/A'

# Function to return file content
def get_raw_file_content(filename):
    text = ""
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            text += file.read()
    return text

# Call the function to return file content
def finding_file_parser(filename, number_of_sections, severity):
    text = get_raw_file_content(filename)
    
    if(text == ""):
        return ""
    
    # Extract the content of each section
    source_content = extract_content('source', 'status', text)
    status_content = extract_content('status', 'commit', text)
    commit_content = extract_content('commit', 'title', text)
    title_content = extract_content('title', 'Description', text)
    description_content = extract_content('Description', 'Exploit Scenario', text)
    exploit_scenario_content = extract_content('Exploit Scenario', 'Remediation', text)
    recommendations_content = extract_content('Recommendations', 'Results', text)
    results_content = extract_content('Results', 'EOF', text)

    # Combine the content of each section
    content = ""

    # title
    content += str(number_of_sections) + ". **" + title_content + "**\n\n"
    # severity
    color = "info" if severity == "Informational" else severity.lower()
    content += '|Severity|<span class=color-{0}>**{1}**</span>|\n|----|----|\n'.format(color, severity)
    # source
    content += '|Source|' + source_content + '|\n'
    # commit
    content += '|Commit|' + commit_content + '|\n'
    # status
    content += '|Status|' + status_content + '|\n\n\n'

    # description
    content += "**Description**\n\n"
    content += description_content + "\n\n"

    # exploit scenario
    content += "**Exploit Scenario**\n\n"
    content += exploit_scenario_content + "\n\n"

    # Recommendations
    content += "**Recommendations**\n\n"
    content += recommendations_content + "\n\n"

    # Results
    content += "**Results**\n\n"
    content += results_content + "\n\n"

    return content


# Call the function to return file content
def title_content_parser(file):
    text = get_raw_file_content(file)

    if(text == ""):
        return ""
    
    # Extract the content of each section
    title_content = extract_content('title', 'content', text)
    content_content = extract_content('content', 'EOF', text)

    # Combine the content of each section
    content = ""

    # title
    content += "## " + title_content + "\n\n"

    # content
    content += content_content + "\n\n"
   
    return content

# Call the function to return file content
def whole_file_parser(filename):
    text = get_raw_file_content(filename)
    return text.replace("EOF", "")

def x_title_content_parser(file_path):
    content = ""

    data = get_raw_file_content(file_path)

    pattern = r"\[title\](.*?)\[content\]"
    title_matches = re.findall(pattern, data, re.DOTALL)

    pattern = r"\[content\](.*?)EOF"
    base_match = re.search(pattern, data, re.DOTALL)

    title_contents = [match.strip() for match in title_matches]
    base_content = base_match.group(1).strip() if base_match else None

    for i in range(len(title_contents)):
        content += '## ' + title_contents[i] + '\n\n'
        content += base_content + '\n\n'

    return content

# print(get_raw_file_content('access-control.md'))
# print(extract_content('title', 'content', get_raw_file_content('access-control.md')))

# print('*******************\n')

# print(get_raw_file_content('project-summary.md'))
# print(extract_content('title', 'content', get_raw_file_content('project-summary.md')))