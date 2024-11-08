import unittest

from utils import (
    TextNode,
    TextType,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        other = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, other)

    def test_not_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        other = TextNode("This is an other text node", TextType.BOLD)
        self.assertNotEqual(node, other)
        other = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, other)
        other = TextNode("This is a text node", TextType.ITALIC, "This is a url")
        self.assertNotEqual(node, other)

    def test_repr(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(
            repr(node), 'TextNode("This is a text node", TextType.BOLD, None)'
        )
        node = TextNode(
            "This is a text node with a url", TextType.ITALIC, "This is a url"
        )
        self.assertEqual(
            repr(node),
            'TextNode("This is a text node with a url", TextType.ITALIC, "This is a url")',
        )

    def test_text_node_to_html_node(self) -> None:
        text_node = TextNode("text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(html_node), 'LeafNode(None, "text", None)')
        self.assertEqual(html_node.to_html(), "text")

        text_node = TextNode("text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(html_node), 'LeafNode("b", "text", None)')
        self.assertEqual(html_node.to_html(), "<b>text</b>")

        text_node = TextNode("text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(html_node), 'LeafNode("i", "text", None)')
        self.assertEqual(html_node.to_html(), "<i>text</i>")

        text_node = TextNode("text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(html_node), 'LeafNode("code", "text", None)')
        self.assertEqual(html_node.to_html(), "<code>text</code>")

        text_node = TextNode("text", TextType.LINK, "url")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), '<a href="url">text</a>')
        text_node = TextNode("text", TextType.LINK)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(repr(html_node), 'LeafNode("a", "text", None)')
        self.assertEqual(html_node.to_html(), "<a>text</a>")

        text_node = TextNode("text", TextType.IMAGE, "url")
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(
            repr(html_node),
            "LeafNode(\"img\", \"\", {'src': 'url', 'alt': 'text'})",
        )
        self.assertEqual(html_node.to_html(), '<img src="url" alt="text"></img>')

    def test_split_nodes_delimiter(self) -> None:
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [repr(n) for n in new_nodes],
            [
                'TextNode("This is text with a ", TextType.TEXT, None)',
                'TextNode("code block", TextType.CODE, None)',
                'TextNode(" word", TextType.TEXT, None)',
            ],
        )

        node = TextNode("This is text with a `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [repr(n) for n in new_nodes],
            [
                'TextNode("This is text with a ", TextType.TEXT, None)',
                'TextNode("code block", TextType.CODE, None)',
            ],
        )

        node = TextNode("This is text with a `code block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            [repr(n) for n in new_nodes],
            [
                'TextNode("This is text with a `code block", TextType.TEXT, None)',
            ],
        )

        node = TextNode(
            "This is **text** with an *italic* word and a `code block`", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            [repr(n) for n in new_nodes],
            [
                'TextNode("This is ", TextType.TEXT, None)',
                'TextNode("text", TextType.BOLD, None)',
                'TextNode(" with an *italic* word and a `code block`", TextType.TEXT, None)',
            ],
        )

        node = TextNode(
            "This is text with an *italic* word and a `code block`", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            [repr(n) for n in new_nodes],
            [
                'TextNode("This is text with an ", TextType.TEXT, None)',
                'TextNode("italic", TextType.ITALIC, None)',
                'TextNode(" word and a `code block`", TextType.TEXT, None)',
            ],
        )

        node = TextNode(
            " with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            [repr(n) for n in new_nodes],
            [
                'TextNode(" with an ", TextType.TEXT, None)',
                'TextNode("italic", TextType.ITALIC, None)',
                'TextNode(" word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)", TextType.TEXT, None)',
            ],
        )

    def test_extract_markdown_images(self) -> None:
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(
            images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

    def test_extract_markdown_links(self) -> None:
        text = "This is text with an image [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(
            links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_split_nodes_image(self) -> None:
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [repr(n) for n in new_nodes],
            [
                'TextNode("This is text with a ", TextType.TEXT, None)',
                'TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif")',
                'TextNode(" and ", TextType.TEXT, None)',
                'TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")',
            ],
        )

    def test_split_nodes_link(self) -> None:
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            [repr(n) for n in new_nodes],
            [
                'TextNode("This is text with a link ", TextType.TEXT, None)',
                'TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")',
                'TextNode(" and ", TextType.TEXT, None)',
                'TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")',
            ],
        )

    def test_text_to_textnodes(self) -> None:
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(
            [repr(n) for n in nodes],
            [
                'TextNode("This is ", TextType.TEXT, None)',
                'TextNode("text", TextType.BOLD, None)',
                'TextNode(" with an ", TextType.TEXT, None)',
                'TextNode("italic", TextType.ITALIC, None)',
                'TextNode(" word and a ", TextType.TEXT, None)',
                'TextNode("code block", TextType.CODE, None)',
                'TextNode(" and an ", TextType.TEXT, None)',
                'TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg")',
                'TextNode(" and a ", TextType.TEXT, None)',
                'TextNode("link", TextType.LINK, "https://boot.dev")',
            ],
        )


if __name__ == "__main__":
    unittest.main()
