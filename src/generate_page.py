import re
import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path


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

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    dest = open(dest_path, "w")
    dest.write(page)
    dest.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for file in os.listdir(dir_path_content):
        content_path = os.path.join(dir_path_content, file)
        content_base = Path(dir_path_content)
        file_path = Path(content_path).relative_to(content_base)

        if os.path.isfile(content_path):
            new_destination = os.path.join(
                dest_dir_path, file_path.with_suffix(".html")
            )
            generate_page(content_path, template_path, new_destination)
        else:
            new_destination = os.path.join(dest_dir_path, file_path)
            generate_pages_recursive(content_path, template_path, new_destination)
