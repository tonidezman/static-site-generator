import unittest
from helpers import markdown_to_blocks, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
        """
        expected_blocks = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        blocks = markdown_to_blocks(text)
        self.assertEqual(blocks, expected_blocks)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_markdown_to_html_node(self):
        text = """
# This is a heading

> This is a quote.

```
print('Hello, World!')
```

* This is an unordered list

1. This is an ordered list

        """
        expected_html = """<div><h1>This is a heading</h1><blockquote>This is a quote.</blockquote><pre><code>
print('Hello, World!')
</code></pre><ul><li>This is an unordered list</li></ul><ol><li>This is an ordered list</li></ol></div>"""
        html = markdown_to_html_node(text)
        self.assertEqual(html.to_html(), expected_html)