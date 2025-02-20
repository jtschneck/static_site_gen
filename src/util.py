import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    ret = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            ret.extend(split_single_text_node(old_node.text, delimiter, text_type))
        else:
            ret.append(old_node)
    return ret

def split_single_text_node(text, delimiter, text_type):
    ret = []

    # Find the first delim (if present)
    split_text = text.split(delimiter, 1)

    # If not present, return node as is
    if len(split_text) == 1:
        return [TextNode(text, TextType.TEXT)]
    
    # Make the first node, if applicable
    beginning, rest = split_text
    if beginning:
        ret.append(TextNode(beginning, TextType.TEXT))
    
    # Find the next delim
    split_text = rest.split(delimiter, 1)

    if len(split_text) == 1:
        raise ValueError(f"No matching delim in '{text}'")
    
    # Make the new node and call recursively on remainder
    ret.append(TextNode(split_text[0], text_type))
    if split_text[1]:
        ret.extend(split_single_text_node(split_text[1], delimiter, text_type))

    return ret

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_link(old_nodes):
    ret = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            link_matches = extract_markdown_links(old_node.text)
            if (link_matches):
                ret.extend(split_node_matches_helper(old_node.text, link_matches, TextType.LINK))
                continue
        ret.append(old_node)
    return ret

def split_nodes_image(old_nodes):
    ret = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            image_matches = extract_markdown_images(old_node.text)
            if (image_matches):
                ret.extend(split_node_matches_helper(old_node.text, image_matches, TextType.IMAGE))
                continue
        ret.append(old_node)
    return ret

def split_node_matches_helper(text, matches, text_type):
    ret = []
    # Get first match
    match_text, url = matches[0]
    # Split on match
    match = f"[{match_text}]({url})"
    if text_type == TextType.IMAGE:
        match = "!" + match
    before, rest = text.split(match, 1)
    # Create text node before special node if needed
    if before:
        ret.append(TextNode(before, TextType.TEXT))
    # Create special node
    ret.append(TextNode(match_text, text_type, url))
    # Call recursively if there's more matches for special nodes
    if len(matches) > 1:
        ret.extend(split_node_matches_helper(rest, matches[1:], text_type))
        return ret
    # Otherwise make a text node if needed
    elif rest:
        ret.append(TextNode(rest, TextType.TEXT))
        return ret
    else:
        return ret