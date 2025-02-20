import unittest
from textnode import *
from util import *

class TestTextNode(unittest.TestCase):
    def test_provided(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        first = TextNode("This is text with a ", TextType.TEXT)
        second = TextNode("code block", TextType.CODE)
        third = TextNode(" word", TextType.TEXT)
        self.assertEqual([first, second, third], new_nodes)

    def test_beginning_empty(self):
        node = TextNode("`code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        second = TextNode("code block", TextType.CODE)
        third = TextNode(" word", TextType.TEXT)
        self.assertEqual([second, third], new_nodes)

    def test_end_empty(self):
        node = TextNode("This is text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        first = TextNode("This is text with a ", TextType.TEXT)
        second = TextNode("code block", TextType.CODE)
        self.assertEqual([first, second], new_nodes)

    def test_multiple_splits(self):
        node = TextNode("This is `text` with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        first = TextNode("This is ", TextType.TEXT)
        second = TextNode("text", TextType.CODE)
        third = TextNode(" with a ", TextType.TEXT)
        fourth = TextNode("code block", TextType.CODE)
        fifth = TextNode(" word", TextType.TEXT)
        self.assertEqual([first, second, third, fourth, fifth], new_nodes)

    def test_unmatched_delim(self):
        node = TextNode("This is `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_split_nodes_link_two_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        res = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
             ),
        ]
        self.assertEqual(res, new_nodes)

    def test_split_nodes_image_two_images(self):
        node = TextNode(
            "This is text with an image ![of boots](boots.png) and ![of youtube](youtube.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        res = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("of boots", TextType.IMAGE, "boots.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "of youtube", TextType.IMAGE, "youtube.png"
             ),
        ]
        self.assertEqual(res, new_nodes)

    def test_split_nodes_image_link(self):
        node = TextNode(
            "This is text with an image ![of boots](boots.png) and a link [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        new_nodes = split_nodes_link(new_nodes)
        res = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("of boots", TextType.IMAGE, "boots.png"),
            TextNode(" and a link ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
             ),
        ]
        self.assertEqual(res, new_nodes)



if __name__ == "__main__":
    unittest.main()