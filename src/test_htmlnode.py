import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self) -> None:
        node = HTMLNode(tag="tag", value="value", children=None, props={"foo": "bar"})
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"foo": "bar"})

    def test_props_to_html(self) -> None:
        node = HTMLNode(
            tag="tag", value="value", children=None, props={"foo": "bar", "baz": "qux"}
        )
        self.assertEqual(node.props_to_html(), ' foo="bar" baz="qux"')

    def test_repr(self) -> None:
        node = HTMLNode(tag="tag", value="value", children=None, props={"foo": "bar"})
        self.assertEqual(
            repr(node), "HTMLNode(\"tag\", \"value\", None, {'foo': 'bar'})"
        )

    def test_leaf_node_init(self) -> None:
        node = LeafNode(tag="tag", value="value")
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_leaf_node_to_html(self) -> None:
        node = LeafNode(tag="tag", value="value")
        self.assertEqual(node.to_html(), "<tag>value</tag>")

        node = LeafNode(tag=None, value="value")
        self.assertEqual(node.to_html(), "value")

    def test_parent_node_init(self) -> None:
        child1 = LeafNode(tag="tag1", value="value1")
        child2 = LeafNode(tag="tag2", value="value2")
        children = [child1, child2]
        node = ParentNode(tag="tag", children=children, props={"foo": "bar"})
        self.assertEqual(node.tag, "tag")
        self.assertEqual(node.value, None)
        self.assertEqual(node.props, {"foo": "bar"})

    def test_parent_node_to_html(self) -> None:
        parent_child = LeafNode(
            tag="parent_child_tag", value="parent_child_value", props={"foo": "bar"}
        )
        parent = ParentNode(tag="parent_tag", children=[parent_child])
        leaf = LeafNode(tag="leaf_tag", value="leaf_value")
        children = [parent, leaf]
        node = ParentNode(tag="tag", children=children)
        self.assertEqual(
            node.to_html(),
            '<tag><parent_tag><parent_child_tag foo="bar">parent_child_value</parent_child_tag></parent_tag><leaf_tag>leaf_value</leaf_tag></tag>',
        )

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

        with self.assertRaises(ValueError):
            node = ParentNode(tag=None, children=None)
            node.to_html()
