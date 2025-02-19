from textnode import TextNode, TextType


def main():
    test = TextNode("This is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    print(test)


main()
