import unittest
from textnode import TextNode, TextType
from helpers import split_nodes_image

class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_image(self):
        text = "This is text with a link ![to boot dev cat](https://www.boot.dev/cat.jpg) and ![to youtube dog](https://www.youtube.com/@bootdotdev/dog.png)"
        node = TextNode(text, TextType.TEXT)
        new_nodes = split_nodes_image([node])

        expected_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev cat", TextType.LINK, "https://www.boot.dev/cat.jpg"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube dog", TextType.LINK, "https://www.youtube.com/@bootdotdev/dog.png"),
        ]
        
        self.assertEqual(new_nodes, expected_nodes)