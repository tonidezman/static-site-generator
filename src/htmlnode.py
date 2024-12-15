from typing import List

class HTMLNode:
    def __init__(
            self,
            tag: str=None,
            value: str=None,
            children: List['HTMLNode']=None,
            props: dict[str, str]=None
            ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join([f'{key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            value: str,
            props: dict[str, str]=None
            ):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.tag is None:
            return self.value
        if self.props is not None and len(self.props) > 0:
            props = " " + self.props_to_html()
        else:
            props = ""
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str,
            children: List[HTMLNode]=None,
            props: dict[str, str]=None
            ):
        if children is None:
            raise ValueError("ParentNode must have children")
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.props is not None and len(self.props) > 0:
            props = " " + self.props_to_html()
        else:
            props = ""
        children = "".join([child.to_html() for child in self.children])
        return f"<{self.tag}{props}>{children}</{self.tag}>"
