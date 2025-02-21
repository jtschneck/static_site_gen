import unittest
from blockutil import *

class TestBlockUtil(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(text)
        expected = ["# This is a heading",
                    ("This is a paragraph of text."
                     " It has some **bold** and *italic* words inside of it."),
                     ("* This is the first list item in a list block\n" +
                        "* This is a list item\n" +
                        "* This is another list item"),
                    ]
        self.assertEqual(expected, blocks)

    def test_markdown_to_blocks_whitespace(self):
        text = """
        
        
        
        
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

                



* This is the first list item in a list block
* This is a list item
* This is another list item
                
                
                
                
                """
        blocks = markdown_to_blocks(text)
        expected = ["# This is a heading",
                    ("This is a paragraph of text."
                     " It has some **bold** and *italic* words inside of it."),
                     ("* This is the first list item in a list block\n" +
                        "* This is a list item\n" +
                        "* This is another list item"),
                    ]
        self.assertEqual(expected, blocks)

    def test_heading(self):
        text = "## Heading"
        self.assertEqual(BlockType.HEADING, block_to_block_type(text))

    def test_not_heading_too_many(self):
        text = "####### Heading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(text))

    def test_not_heading_no_space(self):
        text = "######Heading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(text))

    def test_code_block(self):
        text = "```x = 0```"
        self.assertEqual(BlockType.CODE, block_to_block_type(text))

    def test_not_code_block(self):
        text = "```x = 0``"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(text))

    def test_quote(self):
        text = ">This\n>Is\n>A quote"
        self.assertEqual(BlockType.QUOTE, block_to_block_type(text))
    
    def test_not_quote(self):
        text = ">This\n>Is\nA quote"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(text))

    def test_ulist(self):
        text = "* This\n* Is\n* an unordered list"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(text))

    def test_not_ulist(self):
        text = "* This\n* Is\n>*an unordered list"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(text))

    def test_olist(self):
        text = "1. This\n2. Is\n3. An ordered list"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(text))

    def test_not_olist_bad_numbers(self):
        text = "1. This\n2. Is\n4. An ordered list"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(text))

    def test_not_olist_no_space(self):
        text = "1. This\n2.Is\n3. An ordered list"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(text))




if __name__ == "__main__":
    unittest.main()