import os
import shutil
from pathlib import Path

from utils import generate_pages


def main():
    static_dir = Path("static")
    content_dir = Path("content")
    template_path = Path("template.html")
    public_dir = Path("public")

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    if not os.path.exists(public_dir):
        os.makedirs(public_dir)

    try:
        shutil.rmtree(public_dir)
    except Exception as e:
        print(f"Failed to delete {public_dir}")
        print(e)

    # Copy the source directory to the destination directory
    try:
        shutil.copytree(static_dir, public_dir)
    except Exception as e:
        print(f"Failed to copy {static_dir} to {public_dir}")
        print(e)

    generate_pages(content_dir, template_path, public_dir)


if __name__ == "__main__":
    main()
