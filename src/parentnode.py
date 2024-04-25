from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("Tag required for ParentNode")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")
        child_html = "".join(map(lambda child: child.to_html(), self.children))
        return f"<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>"