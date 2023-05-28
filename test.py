import mistune
import subprocess

markdown_text = """
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
"""


def markdown_to_pdf(input_file, output_file):
    with open(input_file, 'r') as f:
        markdown_text = f.read()

    # Convert Markdown to HTML
    renderer = CustomRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    html_text = markdown(markdown_text)

    # Write the HTML content to a temporary file
    temp_html_file = 'temp.html'
    with open(temp_html_file, 'w') as f:
        f.write(html_text)

    # Use wkhtmltopdf to convert HTML to PDF
    subprocess.run(['wkhtmltopdf', temp_html_file, output_file])

    # Remove the temporary HTML file
    subprocess.run(['rm', temp_html_file])


class CustomRenderer(mistune.Renderer):
    def table(self, header, body):
        return f"<table><thead>{header}</thead><tbody>{body}</tbody></table>"

markdown_to_pdf('head.md', 'out.pdf')