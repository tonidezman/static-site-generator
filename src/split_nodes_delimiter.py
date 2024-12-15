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
