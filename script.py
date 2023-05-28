
import os
from file_parser import finding_file_parser, title_content_parser, whole_file_parser, x_title_content_parser
import pdfkit
import markdown
import subprocess


def markdown_to_pdf(input_file, output_file):
    with open(input_file, 'r') as f:
        markdown_text = f.read()

    # Convert Markdown to HTML
    html_text = markdown.markdown(markdown_text)

    # Write the HTML content to a temporary file
    temp_html_file = 'temp.html'
    with open(temp_html_file, 'w') as f:
        f.write(html_text)

    # Use wkhtmltopdf to convert HTML to PDF
    subprocess.run(['wkhtmltopdf', temp_html_file, output_file])

    # Remove the temporary HTML file
    #subprocess.run(['rm', temp_html_file])

# Example usage
input_file = 'head.md'      # Path to your Markdown file
output_file = 'report.pdf'   # Path to the output PDF file
#markdown_to_pdf('head.md', 'out.pdf')

# Function to combine Markdown files by following these rules shown in the structure file
def write_markdown_files(content, output_filename1, output_filename2):
    with open(output_filename1, 'w') as file1:
        file1.write(content)

    # with open(output_filename2, 'w') as file2:
    #     file2.write(content)

    #convert(output_filename1, output_filename2)

# open the a.md file, read the content, remove EOF mark, and return the content
def extract_content(file):
    with open(file, "r") as file:
        content = file.read().rstrip()
    # Removing the EOF mark if present
    content = content.replace("EOF", "").strip()
    return content

# Function to extract the content of each section
def generate_readme_content():
    content = ""
    # header
    content += whole_file_parser("OtherMarkdown/head.md")

    # about
    content += x_title_content_parser("OtherMarkdown/about.md")

    # table of contents

    content += title_content_parser("OtherMarkdown/service-scope.md")

    # project summary
    content += title_content_parser("OtherMarkdown/project-summary.md")

    # findings bugs
    content += combine_all_findings_files()

    content += title_content_parser("OtherMarkdown/use-case-scenarios.md")
   
    # access control
    content += title_content_parser("OtherMarkdown/access-control.md")

    # access control
    content += title_content_parser("OtherMarkdown/automated-testing.md")

    content += x_title_content_parser("DefaultMarkdown/appendix.md")

    content += x_title_content_parser("DefaultMarkdown/disclaimer.md")

    return content

# search files in the current directory 
# if file name contains "findings" and ends with ".md"
# add the file name to the list of input files
def combine_severity_findings_files(severity):
    findings_content = ""
    findings_content += "### " + "**" + severity + "**\n\n"
    total = 0
    resolved = 0
    acknowledged = 0

    # Find the files with the severity
    mark = "finding-"
    if(severity == "Informational"):
        mark += "info"
    else:
        mark += severity.lower()

    # check files in the current directory
    for file in os.listdir('./'):
        if file.endswith(".md") and mark in file:
            total += 1
            (a, b, content) = finding_file_parser(file, total, severity)
            findings_content += content
            resolved += a
            acknowledged += b

    return (total, resolved, acknowledged, findings_content)


# Function to combine all findings files
def combine_all_findings_files():
    content = ""
    status_content = '''## Findings & Improvement Suggestions

|Severity|**Total**|**Acknowledged**|**Resolved**|
|---|---|---|---|
'''
    severity_list = ["High", "Medium", "Low", "Informational", "Undetermined"]
    for severity in severity_list:
        total, resolved, ackownledged, findings_content = combine_severity_findings_files(severity)
        if total > 0:
            if severity == "Informational":
                color = 'info'
            else:
                color = severity.lower()
            status_content += f"|<span class='color-{color}'>**{severity}**</span>|{total}|{ackownledged}|{resolved}|"
            content += findings_content

    status_content += "\n\n"
    content += "\n\n"
    return status_content + content


# Output Markdown file
output_file1 = "README.md"
output_file2 = "report.pdf"

# Call the function to combine the files
content = generate_readme_content()
write_markdown_files(content, output_file1, output_file2)
def markdown_to_html(input_file, out_file):
    with open(input_file, 'r') as md_file:
        md_content = md_file.read()
        html_content = markdown.markdown(md_content)
        with open(output_file, 'w') as html_file:
            html_file.write(html_content)
        #subprocess.call(['wkhtmltopdf', input_file, output_file])
#markdown_to_html('head.md', 'head.html')
#markdown_to_pdf('head.md', output_file)

#markdown_to_pdf('head.md', output_file)