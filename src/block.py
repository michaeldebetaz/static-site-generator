from enum import Enum


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block != ""]
    return blocks


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("# "):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if (
        block.startswith(">")
        or block.startswith("- ")
        or block.startswith("* ")
        or block.startswith("1. ")
    ):
        lines = block.split("\n")

        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE

        if all(line.startswith("- ") or line.startswith("* ") for line in lines):
            return BlockType.UNORDERED_LIST

        if all(line.startswith(f"{i+1}. ") for i, line in enumerate(lines)):
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
