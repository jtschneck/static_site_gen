import os
import re

from blockutil import *
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from util import split_nodes_delimiter, split_nodes_image, split_nodes_link

def text_to_textnodes(text):
    res = [TextNode(text, TextType.TEXT)]
    # Images must go before links
    res = split_nodes_image(res)
    res = split_nodes_link(res)
    # Bold must go before italics
    res = split_nodes_delimiter(res, "**", TextType.BOLD)
    res = split_nodes_delimiter(res, "*", TextType.ITALIC)
    res = split_nodes_delimiter(res, "`", TextType.CODE)
    return res

def markdown_to_html_node(markdown):
    md_blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for md_block in md_blocks:
        block_type = block_to_block_type(md_block)
        match block_type:
            case BlockType.PARAGRAPH:
                children = text_to_children(md_block)
                html_blocks.append(wrap_with_tag(children, "p"))
            case BlockType.HEADING:
                h_number = md_block.find(" ")
                children = text_to_children(md_block[h_number + 1:])
                html_blocks.append(wrap_with_tag(children, f"h{h_number}"))
            case BlockType.CODE:
                code = LeafNode("code", md_block[3:-3].strip())
                html_blocks.append(wrap_with_tag([code], "pre"))
            case BlockType.QUOTE:
                all_text = [line[2:] for line in md_block.split("\n")]
                children = text_to_children("\n".join(all_text))
                html_blocks.append(wrap_with_tag(children, "blockquote"))
            case BlockType.UNORDERED_LIST:
                list_items_md = [line[2:] for line in md_block.split("\n")]
                list_items_nodes = [wrap_with_tag(text_to_children(line), "li") for line in list_items_md]
                html_blocks.append(wrap_with_tag(list_items_nodes, "ul"))
            case BlockType.ORDERED_LIST:
                list_items_md = [line[line.find(" ") + 1:] for line in md_block.split("\n")]
                list_items_nodes = [wrap_with_tag(text_to_children(line), "li") for line in list_items_md]
                html_blocks.append(wrap_with_tag(list_items_nodes, "ol"))
            case _:
                raise ValueError(f"Unrecognized block type: {block_type}")
    return wrap_with_tag(html_blocks, "div")

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(text_node) for text_node in text_nodes]

def wrap_with_tag(children, tag):
    return ParentNode(tag, children)

def extract_title(markdown):
    res = re.findall(r"^# (.*)", markdown, re.MULTILINE)
    if len(res) < 1:
        raise ValueError("Markdown must contain page title")
    return res[0]

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as file:
        content = file.read()
    with open(template_path, "r") as file:
        template = file.read()
    content_html = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", content_html)
    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok = True)
    with open(dest_path, "w") as file:
        file.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    contents = os.listdir(dir_path_content)
    for path_end in contents:
        src_path = os.path.join(dir_path_content, path_end)
        dest_path = os.path.join(dest_dir_path, path_end)

        # See if it's a markdown file, if so generate a page
        if src_path.endswith(".md") and os.path.isfile(src_path):
            dest_path = dest_path.replace(".md", ".html")
            generate_page(src_path, template_path, dest_path)

        # If it's a directory, recurse
        elif os.path.isdir(src_path):
            generate_pages_recursive(src_path, template_path, dest_path)