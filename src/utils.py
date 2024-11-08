import re
from collections.abc import Sequence
from pathlib import Path

from block import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
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
    for old_node in old_nodes:
        strings = old_node.text.split(delimiter)
        if len(strings) < 3:
            new_nodes.append(old_node)
        else:
            for i, s in enumerate(strings):
                if i % 2 == 0:
                    if len(s) > 0:
                        new_nodes.append(TextNode(s, old_node.text_type))
                if i % 2 != 0:
                    if i == len(strings) - 1:
                        new_nodes.append(TextNode(s, old_node.text_type))
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
            new_nodes.append(old_node)
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
            new_nodes.append(old_node)
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
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes


def text_to_children(text: str) -> Sequence[ParentNode | LeafNode]:
    blocks = markdown_to_blocks(text)

    nodes: Sequence[ParentNode | LeafNode] = []

    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                nodes.append(LeafNode(tag="h1", value=block.lstrip("# ")))

            case BlockType.PARAGRAPH:
                text_nodes = text_to_textnodes(block)
                children = [text_node_to_html_node(t) for t in text_nodes]
                nodes.append(ParentNode(tag="p", children=children))

            case BlockType.CODE:
                nodes.append(LeafNode(tag="code", value=block.strip("```")))

            case BlockType.QUOTE:
                lines = block.split("\n")

                if len(lines) < 2:
                    value = lines[0].lstrip(">").lstrip()
                    children = [LeafNode(tag=None, value=value)]
                else:
                    children = [
                        LeafNode(tag="p", value=line.lstrip(">").lstrip())
                        for line in lines
                    ]

                nodes.append(ParentNode(tag="blockquote", children=children))

            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                list_items: list[ParentNode | LeafNode] = []
                for line in lines:
                    text = line[2:]
                    text_nodes = text_to_textnodes(text)
                    children = [text_node_to_html_node(t) for t in text_nodes]
                    if len(children) < 2:
                        value = children[0].value
                        assert isinstance(value, str)
                        list_items.append(LeafNode(tag="li", value=value))
                    else:
                        list_items.append(ParentNode(tag="li", children=children))
                nodes.append(ParentNode(tag="ul", children=list_items))

            case BlockType.ORDERED_LIST:
                lines = block.split("\n")

                list_items: list[ParentNode | LeafNode] = []
                for line in lines:
                    text = line[3:]
                    text_nodes = text_to_textnodes(text)
                    children = [text_node_to_html_node(t) for t in text_nodes]
                    if len(children) < 2:
                        value = children[0].value
                        assert isinstance(value, str)
                        list_items.append(LeafNode(tag="li", value=value))
                    else:
                        list_items.append(ParentNode(tag="li", children=children))
                nodes.append(ParentNode(tag="ol", children=list_items))

    return nodes


def markdown_to_html_node(markdown: str) -> ParentNode:
    children_nodes = text_to_children(markdown)

    return ParentNode(tag="div", children=children_nodes)


def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    HEADING_PREFIX = "# "

    for block in blocks:
        if block.startswith(HEADING_PREFIX):
            return block.lstrip(HEADING_PREFIX)

    raise Exception("No title found in markdown")


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()
    result = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    if not dest_path.exists():
        dest_path.touch()

    with open(dest_path, "w") as f:
        f.write(result)


def generate_pages(src_path: Path, template_path: Path, dest_path: Path):
    for path in src_path.iterdir():
        if path.is_file():
            name = path.stem
            filename = f"{name}.html"
            generate_page(path, template_path, dest_path / filename)

        if path.is_dir():
            new_dest_path = dest_path / path.name
            new_dest_path.mkdir()
            generate_pages(path, template_path, new_dest_path)
