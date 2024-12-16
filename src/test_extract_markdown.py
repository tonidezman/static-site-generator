import unittest
from helpers import extract_markdown_images, extract_markdown_links, extract_title

class TestExtractMarkupImage(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "![Alt text](http://example.com/image)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("Alt text", "http://example.com/image")])

    def test_extract_markdown_images_2(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpg)"
        images = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpg")
        ]
        self.assertEqual(images, expected)


class TestExtractMarkupLink(unittest.TestCase):
    def test_extract_markdown_images_no_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        images = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(images, expected)

    def test_single_link(self):
        text = "This is a [link](https://example.com)"
        expected = [("link", "https://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "Here is a [link1](https://example1.com) and another [link2](https://example2.com)"
        expected = [("link1", "https://example1.com"), ("link2", "https://example2.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_links(self):
        text = "This text has no links."
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_malformed_links(self):
        text = "This is a [link](htp://example.com) and another [link2](example2.com)"
        expected = []
        self.assertEqual(extract_markdown_links(text), expected)

    def test_links_with_special_characters(self):
        text = "Check this [link](https://example.com/path/to/page@123)"
        expected = [("link", "https://example.com/path/to/page@123")]
        self.assertEqual(extract_markdown_links(text), expected)

class TestExtractTitle(unittest.TestCase):

    def test_valid_title(self):
        markdown = "# Sample Title"
        expected = "Sample Title"
        self.assertEqual(extract_title(markdown), expected)

    def test_no_title(self):
        markdown = "No title here"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_improper_format(self):
        markdown = "## Not a main title"
        with self.assertRaises(ValueError):
            extract_title(markdown)