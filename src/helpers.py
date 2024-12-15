import re
from enum import Enum
from typing import List
from textnode import TextNode, TextType

class BlockType(Enum):
    HEADING = "heading"
    LIST = "list"
    ORDERED_LIST = "ordered_list"
    UNORDERED_LIST = "unordered_list"
    PARAGRAPH = "paragraph"
    CODE = "code"
    QUOTE = "quote"

def block_to_block_type(block: str) -> BlockType:
    """
    Headings start with 1-6 # characters, followed by a space and then the heading text.
    Code blocks must start with 3 backticks and end with 3 backticks.
    Every line in a quote block must start with a > character.
    Every line in an unordered list block must start with a * or - character, followed by a space.
    Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.
    If none of the above conditions are met, the block is a normal paragraph.
    """
    if block.startswith("# "):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith("> ") for line in block.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("* ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i}. ") for i, line in enumerate(block.split("\n"), 1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str) -> List[TextNode]:
    lines = markdown.split("\n\n")
    res = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        res.append(line)
    return res

def text_to_textnodes(text: str) -> List[TextNode]:
    nodes = split_nodes_delimiter([TextNode(text, TextType.TEXT)], "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(
        nodes: List[TextNode],
        delimiter: str,
        new_type: TextType
    ) -> List[TextNode]:
    result = []
    for node in nodes:
        parts = node.text.split(delimiter)
        for i, part in enumerate(parts):
            if part:
                if i % 2 == 0:
                    result.append(TextNode(part, node.text_type))
                else:
                    result.append(TextNode(part, new_type))
    return result

def split_nodes_image(nodes: List[TextNode]) -> List[TextNode]:
    image_pattern = re.compile(r'!\[([^\]]+)\]\(([^)]+)\)')
    new_nodes = []

    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0

        for match in image_pattern.finditer(text):
            start, end = match.span()
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))
            alt_text, url = match.groups()
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            last_index = end

        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes

def split_nodes_link(nodes: List[TextNode]) -> List[TextNode]:
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    new_nodes = []

    for node in nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        last_index = 0

        for match in link_pattern.finditer(text):
            start, end = match.span()
            if start > last_index:
                new_nodes.append(TextNode(text[last_index:start], TextType.TEXT))
            link_text, url = match.groups()
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            last_index = end

        if last_index < len(text):
            new_nodes.append(TextNode(text[last_index:], TextType.TEXT))

    return new_nodes

def extract_markdown_images(text: str) -> List[tuple[str, str]]:
    pattern = r"!\[([\w\s]+)\]\(([\w\:\/\.]+)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> List[tuple[str, str]]:
    pattern = r"\[([\w\s]+)\]\((https:\/\/[\w\.\/@]+)"
    return re.findall(pattern, text)
