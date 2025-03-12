import os
import shutil
import sys
from pathlib import Path

from utils import generate_pages


def main():
    args = sys.argv
    basepath = "/"
    if len(args) > 1:
        basepath = args[1]
    basepath = Path(basepath)
    static_dir = Path("static")
    content_dir = Path("content")
    template_path = Path("template.html")
    docs_dir = Path("docs")

    if os.path.exists(docs_dir):
        shutil.rmtree(docs_dir)

    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)

    try:
        shutil.rmtree(docs_dir)
    except Exception as e:
        print(f"Failed to delete {docs_dir}")
        print(e)

    # Copy the source directory to the destination directory
    try:
        shutil.copytree(static_dir, docs_dir)
    except Exception as e:
        print(f"Failed to copy {static_dir} to {docs_dir}")
        print(e)

    generate_pages(content_dir, template_path, docs_dir, basepath)


if __name__ == "__main__":
    main()
