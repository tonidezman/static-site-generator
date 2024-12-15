import unittest

from enum import Enum
from textnode import TextNode, TextType
from htmlnode import LeafNode
from textnode import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        node2 = TextNode("This is a link", TextType.LINK, "http://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("This is a link", TextType.LINK, "http://example.com")
        node2 = TextNode("This is a link", TextType.LINK, "http://example.org")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, TextType.BOLD, None)")

    # text_node_to_html_node function tests
    def test_text_node_to_html_node_text(self):
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), LeafNode(tag=None, value="This is a text node").to_html())

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), LeafNode(tag="b", value="This is a bold text node").to_html())

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), LeafNode(tag="i", value="This is an italic text node").to_html())

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), LeafNode(tag="code", value="This is a code text node").to_html())

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("This is a link", TextType.LINK, "http://example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), LeafNode(tag="a", value="This is a link", props={"href": "http://example.com"}).to_html())

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("This is an image", TextType.IMAGE, "http://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), LeafNode(tag="img", value="This is an image", props={"src": "http://example.com/image.png"}).to_html())

if __name__ == "__main__":
    unittest.main()
