import unittest
from textnode import TextNode, TextType
from split_nodes_delimiter import split_nodes_delimiter

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is text without delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected_nodes = [
            TextNode("This is text without delimiter", TextType.TEXT),
        ]
        
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("This is `text` with `multiple` delimiters", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.CODE),
            TextNode(" with ", TextType.TEXT),
            TextNode("multiple", TextType.CODE),
            TextNode(" delimiters", TextType.TEXT),
        ]
        
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_at_beginning(self):
        node = TextNode("`code block` at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected_nodes = [
            TextNode("code block", TextType.CODE),
            TextNode(" at the beginning", TextType.TEXT),
        ]
        
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_nodes_delimiter_at_end(self):
        node = TextNode("Text at the end `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected_nodes = [
            TextNode("Text at the end ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
        ]
        
        self.assertEqual(new_nodes, expected_nodes)

if __name__ == "__main__":
    unittest.main()