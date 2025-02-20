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




if __name__ == "__main__":
    unittest.main()