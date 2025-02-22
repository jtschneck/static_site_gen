import os
import shutil

from converter import generate_pages_recursive

def main():
    copy_public_to_static()
    generate_pages_recursive("content", "template.html", "public")

def copy_public_to_static():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copy_dir_recursive("static", "public")

def copy_dir_recursive(src, dest):
    contents = os.listdir(src)
    for path_end in contents:
        src_path = os.path.join(src, path_end)
        dest_path = os.path.join(dest, path_end)
        # If it's a file, copy it and move on
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)

        # If it's a directory, make a new one and call recursively
        elif os.path.isdir(src_path):
            os.mkdir(dest_path)
            copy_dir_recursive(src_path, dest_path)

main()