import unittest

from converter import *

class TestConverter(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        res = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(expected, res)

    def test_text_to_textnodes_all_text(self):
        text = "this is only text"
        res = text_to_textnodes(text)
        expected = [TextNode(text, TextType.TEXT)]
        self.assertEqual(expected, res)

    def test_md_to_html_empty(self):
        text = ""
        expected = "<div></div>"
        res = markdown_to_html_node(text).to_html()
        self.assertEqual(expected, res)

    def test_md_to_html_basic(self):
        text = "single paragraph"
        expected = "<div><p>single paragraph</p></div>"
        res = markdown_to_html_node(text).to_html()
        self.assertEqual(expected, res)

    def test_md_to_html_two_paragraphs(self):
        text = "single paragraph\n\nsecond paragraph"
        expected = "<div><p>single paragraph</p><p>second paragraph</p></div>"
        res = markdown_to_html_node(text).to_html()
        self.assertEqual(expected, res)

    def test_md_to_html_ul(self):
        text = "* First\n* Second"
        expected = "<div><ul><li>First</li><li>Second</li></ul></div>"
        res = markdown_to_html_node(text).to_html()
        self.assertEqual(expected, res)

    def test_md_to_html_ul_bold(self):
        text = "* First\n* **Second**"
        expected = "<div><ul><li>First</li><li><b>Second</b></li></ul></div>"
        res = markdown_to_html_node(text).to_html()
        self.assertEqual(expected, res)

    def test_md_to_html_ol(self):
        text = "1. First\n2. Second"
        expected = "<div><ol><li>First</li><li>Second</li></ol></div>"
        res = markdown_to_html_node(text).to_html()
        self.assertEqual(expected, res)

    def test_md_to_html_quote(self):
        text = "> one line\n> two lines"
        expected = "<div><blockquote>one line\ntwo lines</blockquote></div>"
        res = markdown_to_html_node(text).to_html()
        self.assertEqual(expected, res)

    def test_md_to_html_code(self):
        text = "```code```"
        expected = "<div><pre><code>code</code></pre></div>"
        res = markdown_to_html_node(text).to_html()
        self.assertEqual(expected, res)

    def test_md_to_html_heading(self):
        text = "##### Heading"
        expected = "<div><h5>Heading</h5></div>"
        res = markdown_to_html_node(text).to_html()
        self.assertEqual(expected, res)

    def test_extract_title(self):
        res = extract_title("# Hello")
        self.assertEqual("Hello", res)

    def test_extract_title_error(self):
        with self.assertRaises(ValueError):
            res = extract_title("## Hello")

if __name__ == "__main__":
    unittest.main()