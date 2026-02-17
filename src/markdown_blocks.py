import re
import textwrap
from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_blocks(markdown):
    parts = re.split(r"\n\s*\n", markdown.strip())
    return [p.strip() for p in parts if p.strip()]

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


# convert full markdown into single HTMLNode
def markdown_to_html_node(markdown):
    html_converted_from_markdown = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        bloktyp = block_to_block_type(block)

        if bloktyp == BlockType.HEADING:
            html_converted_from_markdown.append(heading_to_html_node(block))
        elif bloktyp == BlockType.CODE:
            html_converted_from_markdown.append(code_to_html_node(block))
        elif bloktyp == BlockType.QUOTE:
            html_converted_from_markdown.append(quote_to_html_node(block))
        elif bloktyp == BlockType.UNORDERED_LIST:
            html_converted_from_markdown.append(unordered_list_to_html_node(block))
        elif bloktyp == BlockType.ORDERED_LIST:
            html_converted_from_markdown.append(ordered_list_to_html_node(block))
        elif bloktyp == BlockType.PARAGRAPH :
            html_converted_from_markdown.append(paragraph_to_html_node(block))

    return ParentNode("div", html_converted_from_markdown)

def heading_to_html_node(block: str):
    # block looks like: "### My title"
    i = 0
    while i < len(block) and block[i] == "#":
        i += 1
    level = i  # should be 1..6 for valid headings
    text = block[level:].lstrip()  # remove the leading #'s, then the space
    return ParentNode(f"h{level}", text_to_children(text))

import textwrap

def code_to_html_node(block: str):
    lines = block.split("\n")
    content = "\n".join(lines[1:-1])
    content = textwrap.dedent(content) + "\n"
    code_child = text_node_to_html_node(TextNode(content, TextType.TEXT))
    return ParentNode("pre", [ParentNode("code", [code_child])])

def quote_to_html_node(block: str):
    lines = block.split("\n")
    cleaned = []
    for line in lines:
        # line should start with ">"
        line = line[1:]  # drop the ">"
        if line.startswith(" "):
            line = line[1:]  # drop one optional space
        cleaned.append(line)

    content = " ".join(cleaned)  # quote blocks become one paragraph-ish text
    return ParentNode("blockquote", text_to_children(content))

def unordered_list_to_html_node(block: str):
    lines = block.split("\n")
    items = []
    for line in lines:
        item_text = line[2:]
        items.append(ParentNode("li", text_to_children(item_text)))

    return ParentNode("ul", items)

def ordered_list_to_html_node(block: str):
    lines = block.split("\n")
    items = []
    for line in lines:
        _, item_text = line.split(". ", 1)
        items.append(ParentNode("li", text_to_children(item_text)))
    return ParentNode("ol", items)

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph_text = " ".join(line.strip() for line in lines)
    return ParentNode("p", text_to_children(paragraph_text))

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children
