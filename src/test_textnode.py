import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "")
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode("This is a text node", TextType.BOLD, "www")
        node2 = TextNode("This is a text node", TextType.BOLD, "www")
        self.assertEqual(node, node2)

    def test_eq4(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        txt = repr(node)
        self.assertEqual("TextNode(This is a text node, bold, None)", txt)

    def test_convert_text(self):
        node = TextNode("Text", TextType.TEXT)
        html = text_node_to_html_node(node).to_html()
        self.assertEqual("Text", html)

    def test_convert_bold(self):
        node = TextNode("Text", TextType.BOLD)
        html = text_node_to_html_node(node).to_html()
        self.assertEqual("<b>Text</b>", html)

    def test_convert_italic(self):
        node = TextNode("Text", TextType.ITALIC)
        html = text_node_to_html_node(node).to_html()
        self.assertEqual("<i>Text</i>", html)

    def test_convert_code(self):
        node = TextNode("Text", TextType.CODE)
        html = text_node_to_html_node(node).to_html()
        self.assertEqual("<code>Text</code>", html)

    def test_convert_link(self):
        node = TextNode("Text", TextType.LINK, "https://www.google.com")
        html = text_node_to_html_node(node).to_html()
        self.assertEqual('<a href="https://www.google.com">Text</a>', html)

    def test_convert_image(self):
        node = TextNode("Text", TextType.IMAGE, "https://www.google.com")
        html = text_node_to_html_node(node).to_html()
        self.assertEqual('<img src="https://www.google.com" alt="">Text</img>', html)


if __name__ == "__main__":
    unittest.main()