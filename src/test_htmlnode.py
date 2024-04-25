import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props = {"a":"b", "c":"d"})
        html = ' a="b" c="d"'
        self.assertEqual(html, node.props_to_html())

    def test_props_to_html2(self):
        node = HTMLNode(props = {"href": "https://www.google.com", "target": "_blank"})
        html = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(html, node.props_to_html())

    def test_none_props(self):
        node = HTMLNode()
        self.assertEqual("", node.props_to_html())

if __name__ == "__main__":
    unittest.main()