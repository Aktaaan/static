# from textnode import TextNode
import sys
from copystatic import copy_directory
from gencontent import generate_page
from gencontent import generate_pages_recursive


def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    source_path = "./static"
    destination_path = "./docs"

    copy_directory(source_path, destination_path)

    generate_pages_recursive("content", "template.html", destination_path, basepath)


main()
