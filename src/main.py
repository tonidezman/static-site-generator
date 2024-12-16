import os
import shutil
from textnode import TextNode, TextType

def main():
    copy_static_files_to_public_folder()

def copy_static_files_to_public_folder():
    if not os.path.exists("public"):
        os.makedirs("public")

    if os.path.exists("public"):
        for item in os.listdir("public"):
            item_path = os.path.join("public", item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

    for root, dirs, files in os.walk("static"):
        relative_root = os.path.relpath(root, "static")
        for directory in dirs:
            dest_dir = os.path.join("public", relative_root, directory)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)

        for file in files:
            src_path = os.path.join(root, file)
            relative_root = os.path.relpath(root, "static")
            dest_path = os.path.join("public", relative_root, file)
            shutil.copy(src_path, dest_path)
    
    

if __name__ == "__main__":
    main()
