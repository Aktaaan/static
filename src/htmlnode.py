class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        ret_string = []
        if self.props == None:
            return ""
        for prop in self.props:
            ret_string.append(f' {prop}=\"{self.props[prop]}"')
        finished_reformat = "".join(ret_string)
        return finished_reformat

    def __repr__(self):
        return f'"HTMLNode({self.tag}": "{self.value}", \n"{self.children}": "{self.props}")'

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("No value provided")
        if self.tag is None:
            return(self.value)
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag is None:
            raise ValueError("No tag provided")
        if self.children is None:
            raise ValueError("No children provided")
        else:
            list_for_return = []
            for child in self.children:
                list_for_return.append(child.to_html())
            joined_list = "".join(list_for_return)
            return f"<{self.tag}>{joined_list}</{self.tag}>"

