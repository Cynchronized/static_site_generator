import os
import shutil
from generate_page import generate_page, generate_pages_recursive


dir_path_public = "./public"
dir_path_static = "./static"
dir_path_content = "./content"
dir_path_dest = "./public"
dir_path_template = "./template.html"


def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_source_directory_to_destination("./static", "./public")

    generate_pages_recursive(dir_path_content, dir_path_template, dir_path_dest)


def copy_source_directory_to_destination(source, destination):
    if not os.path.exists(source):
        raise Exception(f"source path could not be found: ${source}")
    if not os.path.exists(destination):
        os.mkdir(destination)

    for file in os.listdir(source):
        source_path = os.path.join(source, file)
        new_destination = os.path.join(destination, file)

        print(f"Copying: {source_path} to {new_destination}")

        if os.path.isfile(source_path):
            shutil.copy(source_path, os.path.join(destination, file))
        else:
            copy_source_directory_to_destination(source_path, new_destination)


main()
