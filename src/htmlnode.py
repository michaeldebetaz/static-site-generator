from typing import Sequence


class HTMLNode:
    def __init__(
        self,
        tag: str | None,
        value: str | None,
        children: Sequence["LeafNode | ParentNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return "".join([f' {k}="{v}"' for k, v in self.props.items()])

    def __repr__(self) -> str:
        tag = f'"{self.tag}"' if self.tag is not None else "None"
        value = f'"{self.value}"' if self.value is not None else "None"
        return f"HTMLNode({tag}, {value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, None, props)
        if self.children is not None:
            raise ValueError("Leaf nodes cannot have children")

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("Leaf nodes must have a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        tag = f'"{self.tag}"' if self.tag is not None else "None"
        return f'LeafNode({tag}, "{self.value}", {self.props})'


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: Sequence["LeafNode | ParentNode"],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)
        if self.value is not None:
            raise ValueError("Parent nodes cannot have a value")
        self.children = children

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Parent nodes must have a tag")
        if self.children is None:
            raise ValueError("Parent nodes must have children")
        return f"<{self.tag}{self.props_to_html()}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"

    def __repr__(self) -> str:
        return f'ParentNode("{self.tag}", {self.children}, {self.props})'
