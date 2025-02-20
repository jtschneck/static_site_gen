from textnode import TextNode, TextType
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
