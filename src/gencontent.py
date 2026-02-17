import os
from markdown_blocks import *

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            cleaned_line = line[2:]
            return cleaned_line.strip()

    raise Exception("no header")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md_frompath = from_path
    md_templatepath = template_path
    markdown_object = open(f"{md_frompath}", "r")
    markdown_content = markdown_object.read()
    template_object = open(f"{md_templatepath}", "r")
    template_content = template_object.read()

    root_node = markdown_to_html_node(markdown_content)
    html_node = root_node.to_html()
    title = extract_title(markdown_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_node)
    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    directory_path = os.path.dirname(dest_path)
    if directory_path != "":
        os.makedirs(directory_path, exist_ok=True)
    file_object = open(dest_path, "w")
    file_object.write(template_content)
    file_object.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    list_everything = os.listdir(dir_path_content)
    for file in list_everything:
        file_path = os.path.join(dir_path_content, file)
        get_the_freaking_job_done_path = os.path.join(dest_dir_path, file.replace(".md", ".html"))
        if file.endswith(".md"):
            generate_page(file_path, template_path, get_the_freaking_job_done_path, basepath)
        elif os.path.isdir(file_path):
            generate_pages_recursive(file_path, template_path, get_the_freaking_job_done_path, basepath)