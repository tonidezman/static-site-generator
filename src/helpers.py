import re
from typing import List
from textnode import TextNode, TextType

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
            new_nodes.append(TextNode(alt_text, TextType.LINK, url))
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
