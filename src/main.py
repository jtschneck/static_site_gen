from textnode import TextNode, TextType

def main():
    node = TextNode("Test node", TextType.BOLD, "wikipedia.org")
    print(node)

main()