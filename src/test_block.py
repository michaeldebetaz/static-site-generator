import unittest
from unittest import TestCase

from block import BlockType, block_to_block_type, markdown_to_blocks
from utils import markdown_to_html_node


class TestBlock(TestCase):
    def test_markdown_to_blocks(self) -> None:
        markdown = "# This is a heading\n\n This is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n   * This is the first list item in a list block\n* This is a list item\n* This isanother list item"
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This isanother list item",
            ],
        )

    def test_block_to_block_type(self) -> None:
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "#This is not a heading"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)

        block = "```python\nprint('Hello, World!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "``\nprint('Hello, World!')\n`"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)
        block = "```python\nprint('Hello, World!')\n"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)
        block = "print('Hello, World!')\n```"
        self.assertNotEqual(block_to_block_type(block), BlockType.CODE)

        block = "> This is a quote block\n> This is another quote block"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = ">This is a quote line\nThis is not a quote line"
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "* This is the first list item in a list block\n* This is a list item\n* This isanother list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "*This is a list item\n*This isanother list item"
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- This is another list item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "-This is a list item"
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "1. This is the first list item in a list block\n2. This is a list item\n3. This isanother list item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1.This is a list item\n1.This isanother list item"
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "This is a paragraph of text. It has some **bold** and *italic* words inside of it."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_markdown_to_html_node(self) -> None:
        markdown = "# heading\n\nParagraph with **bold** and *italic*\n\n* A list item\n* Another list item\n\n*Not a list item\n\n1. A first list item\n2. A second list item\n\n3. Not a list item\n\n```A code block```\n\n>A quote line\n>an other quote line\n\n\n\n"
        nodes = markdown_to_html_node(markdown)

        self.assertEqual(
            nodes.to_html(),
            "<div><h1>heading</h1><p>Paragraph with <b>bold</b> and <i>italic</i></p><ul><li>A list item</li><li>Another list item</li></ul><p>*Not a list item</p><ol><li>A first list item</li><li>A second list item</li></ol><p>3. Not a list item</p><code>A code block</code><blockquote><p>A quote line</p><p>an other quote line</p></blockquote></div>",
        )


if __name__ == "__main__":
    unittest.main()
