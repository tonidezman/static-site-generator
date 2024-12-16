import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_node(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_node_with_tag(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_node_with_value(self):
        node = HTMLNode(value="Hello")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_node_with_children(self):
        child = HTMLNode(tag="span", value="Child")
        node = HTMLNode(tag="div", children=[child])
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "span")
        self.assertEqual(node.children[0].value, "Child")
        self.assertIsNone(node.props)

    def test_node_with_props(self):
        node = HTMLNode(tag="div", props={"class": "container"})
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"class": "container"})

    def test_props_to_html(self):
        node = HTMLNode(tag="div", props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), 'class="container" id="main"')

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div")
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode(tag="div", value="Hello", props={"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(div, Hello, None, {'class': 'container'})")

    def test_node_with_empty_children_list(self):
        node = HTMLNode(tag="div", children=[])
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, [])
        self.assertIsNone(node.props)

    def test_node_with_empty_props_dict(self):
        node = HTMLNode(tag="div", props={})
        self.assertEqual(node.tag, "div")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {})

class TestLeafNode(unittest.TestCase):
    def test_leaf_node_with_tag_and_value(self):
        node = LeafNode(tag="p", value="Hello")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertEqual(node.to_html(), '<p>Hello</p>')

    def test_leaf_node_with_props(self):
        node = LeafNode(tag="img", value="", props={"src": "image.png", "alt": "An image"})
        self.assertEqual(node.tag, "img")
        self.assertEqual(node.value, "")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"src": "image.png", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="An image"></img>')

    def test_leaf_node_with_empty_props(self):
        node = LeafNode(tag="br", value="", props={})
        self.assertEqual(node.tag, "br")
        self.assertEqual(node.value, "")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {})
        self.assertEqual(node.to_html(), '<br></br>')

    def test_leaf_node_repr(self):
        node = LeafNode(tag="span", value="Text", props={"class": "highlight"})
        self.assertEqual(repr(node), "HTMLNode(span, Text, None, {'class': 'highlight'})")

    def test_leaf_node_without_value_raises_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value=None)

    def test_leaf_node_with_empty_value(self):
        node = LeafNode(tag="p", value="")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertEqual(node.to_html(), '<p></p>')

    def test_leaf_node_with_special_characters_in_value(self):
        node = LeafNode(tag="p", value="<Hello & Welcome>")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "<Hello & Welcome>")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertEqual(node.to_html(), '<p><Hello & Welcome></p>')

    def test_leaf_node_without_tag_returns_raw_text(self):
        node = LeafNode(tag=None, value="Raw text")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Raw text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertEqual(node.to_html(), "Raw text")

class TestParentNode(unittest.TestCase):
    def test_parent_node_with_multiple_children(self):
        child1 = LeafNode(tag="span", value="Child 1")
        child2 = LeafNode(tag="span", value="Child 2")
        parent = ParentNode(tag="div", children=[child1, child2])
        self.assertEqual(parent.tag, "div")
        self.assertIsNone(parent.value)
        self.assertEqual(len(parent.children), 2)
        self.assertEqual(parent.children[0].tag, "span")
        self.assertEqual(parent.children[0].value, "Child 1")
        self.assertEqual(parent.children[1].tag, "span")
        self.assertEqual(parent.children[1].value, "Child 2")
        self.assertIsNone(parent.props)
        self.assertEqual(parent.to_html(), '<div><span>Child 1</span><span>Child 2</span></div>')

    def test_parent_node_with_no_children_raises_value_error(self):
        with self.assertRaises(ValueError):
            ParentNode(tag="div", children=None)

    def test_parent_node_with_one_child(self):
        child = LeafNode(tag="span", value="Child")
        parent = ParentNode(tag="div", children=[child])
        self.assertEqual(parent.tag, "div")
        self.assertIsNone(parent.value)
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0].tag, "span")
        self.assertEqual(parent.children[0].value, "Child")
        self.assertIsNone(parent.props)
        self.assertEqual(parent.to_html(), '<div><span>Child</span></div>')

    def test_parent_node_with_props(self):
        child = LeafNode(tag="span", value="Child")
        parent = ParentNode(tag="div", children=[child], props={"class": "container"})
        self.assertEqual(parent.tag, "div")
        self.assertIsNone(parent.value)
        self.assertEqual(len(parent.children), 1)
        self.assertEqual(parent.children[0].tag, "span")
        self.assertEqual(parent.children[0].value, "Child")
        self.assertEqual(parent.props, {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>Child</span></div>')

    def test_parent_node_without_tag_raises_value_error(self):
        child = LeafNode(tag="span", value="Child")
        with self.assertRaises(ValueError):
            ParentNode(tag=None, children=[child]).to_html()

    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            'class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, None, {'class': 'primary'})",
        )

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
