import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        html = "<p>This is a paragraph of text.</p>"
        self.assertEqual(html, node.to_html())

    def test_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(html, node.to_html())

if __name__ == "__main__":
    unittest.main()