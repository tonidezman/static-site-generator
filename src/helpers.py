import re
import os
from enum import Enum
from typing import List
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

class BlockType(Enum):
    HEADING = 1
    LIST = 2
    ORDERED_LIST = 3
    UNORDERED_LIST = 4
    PARAGRAPH = 5
    CODE = 6
    QUOTE = 7

def generate_pages_recursive(from_path: str, template_path: str, dest_path: str):
    if os.path.isfile(from_path):
        dest_path = os.path.splitext(dest_path)[0] + '.html'
        generate_page(from_path, template_path, dest_path)
    elif os.path.isdir(from_path):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        for item in os.listdir(from_path):
            item_path = os.path.join(from_path, item)
            relative_item_path = os.path.relpath(item_path, from_path)
            new_dest_path = os.path.join(dest_path, relative_item_path)
            generate_pages_recursive(item_path, template_path, new_dest_path)

def generate_page(from_path: str, template_path: str, dest_path: str):
    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()
    heading = extract_title(markdown)
    html = markdown_to_html_node(markdown)
    with open(dest_path, "w") as f:
        template = template.replace("{{ Title }}", heading)
        template = template.replace("{{ Content }}", html.to_html())
        f.write(template)

def block_to_block_type(block: str) -> BlockType:
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
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
    blocks = markdown.split("\n\n")
    res = []
    for block in blocks:
        block = block.strip()
        if block == "":
            continue
        res.append(block)
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

def extract_title(markdown: str) -> str:
    if markdown.startswith("# "):
        # Find the first newline
        return markdown[2:markdown.index("\n")].strip()
    else:
        raise ValueError("No title found")

def extract_markdown_images(text: str) -> List[tuple[str, str]]:
    pattern = r"!\[([\w\s]+)\]\(([\w\:\/\.]+)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> List[tuple[str, str]]:
    pattern = r"\[([\w\s]+)\]\((https:\/\/[\w\.\/@]+)"
    return re.findall(pattern, text)

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.HEADING:
            level = block.count("#")
            tag = f"h{level}"
            nodes.append(ParentNode(tag=tag, children=text_to_textnodes(block[level + 1:].strip())))
        elif block_type == BlockType.CODE:
            nodes.append(ParentNode(tag="pre", children=[LeafNode(tag="code", value=block[3:-3])]))
        elif block_type == BlockType.QUOTE:
            nodes.append(ParentNode(tag="blockquote", children=text_to_textnodes(block[2:].strip())))
        elif block_type == BlockType.UNORDERED_LIST:
            children = [ParentNode(tag="li", children=text_to_textnodes(line[2:].strip())) for line in block.split("\n")]
            nodes.append(ParentNode(tag="ul", children=children))
        elif block_type == BlockType.ORDERED_LIST:
            children = [ParentNode(tag="li", children=text_to_textnodes(line.split(". ")[1].strip())) for line in block.split("\n")]
            nodes.append(ParentNode(tag="ol", children=children))
        else:
            nodes.append(ParentNode(tag="p", children=text_to_textnodes(block)))
    root = ParentNode(tag="div", children=nodes)
    return root