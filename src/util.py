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