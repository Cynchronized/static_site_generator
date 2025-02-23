from enum import Enum
from htmlnode import ParentNode
import re

from markdown_parser import text_to_textnodes
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_html_node(markdown):
    children = []
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    elif block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    elif block_type == BlockType.CODE:
        return code_to_html_node(block)
    elif block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    elif block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)

    raise ValueError("invalid block type")


def paragraph_to_html_node(block):
    lines = block.strip().split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = block.count("#")
    if level + 1 >= len(block):
        return ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```" or not block.endswith("```")):
        raise ValueError("invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code_node = ParentNode("code", children)
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())

    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def unordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ul", html_items)


def ordered_list_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))

    return ParentNode("ol", html_items)


def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)

    return html_nodes


# Uses regex to returnt the block type of a given block
def block_to_block_type(block):
    heading_block = re.findall(r"^(#{1,6})\s+(.+)$", block)
    code_block = re.findall(r"^```(?:\s*(\w+))?\n([\s\S]*?)\n```$", block, re.MULTILINE)
    quote_block = check_if_matches_block_pattern(block, r"^>\s*(.+)$")
    unordered_list = check_if_matches_block_pattern(block, r"^\s*[-+*]\s+(.+)$")
    ordered_list = check_if_ordered_list(block)

    if len(heading_block) > 0:
        return BlockType.HEADING
    elif len(code_block) > 0:
        return BlockType.CODE
    elif quote_block:
        return BlockType.QUOTE
    elif unordered_list:
        return BlockType.UNORDERED_LIST
    elif ordered_list:
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def check_if_matches_block_pattern(block, pattern):
    lines = block.split("\n")
    for line in lines:
        match = re.findall(f"{pattern}", line)
        if not match:
            return False

    return True


def check_if_ordered_list(block):
    for i, line in enumerate(
        block.split("\n"),
    ):
        match = re.findall(rf"^\s*{i + 1}\.\s+(.+)$", line)
        if not match:
            return False
    return True


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks
