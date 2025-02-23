import re
import shutil
import os
from markdown_blocks import markdown_to_html_node


# Extract the title by the h1 header
def extract_title(markdown):
    h1 = re.search(r"^#{1}\s.+$", markdown, re.MULTILINE)
    if not h1:
        raise Exception("markdown needs a valid h1 header")

    return h1.group().lstrip("# ").strip()


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path, "r")
    markdown = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    markdown_file.close()

    node = markdown_to_html_node(markdown)
    html_string = node.to_html()

    title = extract_title(markdown)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_string)

    if not os.path.dirname(dest_path):
        os.makedirs(dest_path)

    dest = open(dest_path, "w")
    dest.write(page)
