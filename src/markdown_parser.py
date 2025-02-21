from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text_type is not TextType.NORMAL_TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)

            if len(split_text) % 2 == 0:
                raise Exception("Error: Invalid Markdown syntax")

            for i, chunk in enumerate(split_text):
                if chunk:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(chunk, TextType.NORMAL_TEXT))
                    else:
                        new_nodes.append(TextNode(chunk, text_type))

    return new_nodes


# Regex dark magic to extract markdonw images
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# Regex dark magic to extract markdown links
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
