import re

from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            props = {"href": text_node.url} if text_node.url is not None else None
            return LeafNode(tag="a", value=text_node.text, props=props)
        case TextType.IMAGE:
            props = {}
            if text_node.url is not None:
                props["src"] = text_node.url
            props["alt"] = text_node.text
            return LeafNode(tag="img", value="", props=props)
        case _:
            raise Exception("Invalid text type")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        print(f"\n{node.text}")
        strings = node.text.split(delimiter)
        if len(strings) < 3:
            new_nodes = old_nodes.copy()
        else:
            for i, s in enumerate(strings):
                print(f"\n{i=} --- {s=}")
                if i % 2 == 0:
                    if len(s) > 0:
                        new_nodes.append(TextNode(s, node.text_type))
                if i % 2 != 0:
                    if i == len(strings) - 1:
                        new_nodes.append(TextNode(s, node.text_type))
                    else:
                        new_nodes.append(TextNode(s, text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\]]*)\]\(([^\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\]]*)\]\(([^\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        if len(images) < 1:
            new_nodes = old_nodes.copy()
        else:
            text_so_far = old_node.text
            for image in images:
                alt, url = image
                strings = text_so_far.split(f"![{alt}]({url})")

                prev_str = strings[0]
                next_str = strings[1]
                if len(prev_str) > 0:
                    new_nodes.append(TextNode(prev_str, old_node.text_type))
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))
                text_so_far = next_str

            if len(text_so_far) > 0:
                new_nodes.append(TextNode(text_so_far, old_node.text_type))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        if len(links) < 1:
            new_nodes = old_nodes.copy()
        else:
            text_so_far = old_node.text
            for link in links:
                text, url = link
                strings = text_so_far.split(f"[{text}]({url})")

                prev_str = strings[0]
                next_str = strings[1]
                if len(prev_str) > 0:
                    new_nodes.append(TextNode(prev_str, old_node.text_type))
                new_nodes.append(TextNode(text, TextType.LINK, url))
                text_so_far = next_str

            if len(text_so_far) > 0:
                new_nodes.append(TextNode(text_so_far, old_node.text_type))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]
    print("\n-------------------")
    print("Original:")
    print(nodes)
    print("-------------------\n")
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    print("\n-------------------")
    print("Bold:")
    print(nodes)
    print("-------------------\n")
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    print("\n-------------------")
    print("Italic:")
    print(nodes)
    print("-------------------\n")
    # nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    # print("\n-------------------")
    # print("Code:")
    # print(nodes)
    # print("-------------------\n")
    # nodes = split_nodes_image(nodes)
    # print("\n-------------------")
    # print("Image:")
    # print(nodes)
    # print("-------------------\n")
    # nodes = split_nodes_link(nodes)
    # print("\n-------------------")
    # print("Link:")
    # print(nodes)
    # print("-------------------\n")
    return nodes