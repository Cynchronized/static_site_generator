from textnode import TextType, TextNode
import re


# Converts a raw string of markdown into a list of TextNode objects
def text_to_textnodes(text):
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes


# Converts a raw markdown string into a list of TextNode objects for bold, italic modifers
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        # Only want to split "text" type objects not bold, italtic, etc
        if node.text_type is not TextType.TEXT:
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
                        new_nodes.append(TextNode(chunk, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(chunk, text_type))

    return new_nodes


# Splits a raw markdown text that contains images into multiple TextNode Objects
def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        images = extract_markdown_images(text)
        # If there are no images just return the old node
        if len(images) == 0:
            new_nodes.append(node)
            continue

        for image in images:
            # Sections will be [{normal_text}, {image}, {rest_of_text}]
            sections = text.split(f"![{image[0]}]({image[1]})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )

            text = sections[1]

        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


# Splits a raw markdown text that contains links into multiple TextNode objects
def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        links = extract_markdown_links(original_text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)

            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(
                TextNode(
                    link[0],
                    TextType.LINK,
                    link[1],
                )
            )
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


# Regex dark magic to extract markdown images
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


# Regex dark magic to extract markdown links
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
