from textnode import TextType, TextNode
import re


# Converts a raw markdown string into a list of TextNode objects
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only want to split "text" type objects not bold, italtic, etc
        if node.text_type is not TextType.NORMAL_TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)

            # If there isn't a closing delimiter, the text will split into an even number, thus invalid marldown
            if len(split_text) % 2 == 0:
                raise Exception("Error: Invalid Markdown syntax")

            # The normal text will always be indexed on an even number,
            # inline elements such as bold, code, italic will be indexed on an odd number
            for i, chunk in enumerate(split_text):
                if chunk:
                    if i % 2 == 0:
                        new_nodes.append(TextNode(chunk, TextType.NORMAL_TEXT))
                    else:
                        new_nodes.append(TextNode(chunk, text_type))

    return new_nodes


# TODO: split_nodes_images and split_nodes_link


# Regex dark magic to extract markdonw images
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# Regex dark magic to extract markdown links
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
