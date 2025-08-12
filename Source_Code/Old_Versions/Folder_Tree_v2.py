import os
from pathlib import Path

def print_tree(path: Path, prefix=""):
    """
    Recursively prints a directory tree structure.
    This function will include ALL folders and subfolders without skipping.

    Args:
        path (Path): Pathlib Path object for directory or file.
        prefix (str): Indentation and tree branch characters for hierarchy view.
    """
    # Display current folder/file name
    print(prefix + path.name + ("/" if path.is_dir() else ""))

    # If it's a directory, iterate over its children
    if path.is_dir():
        children = sorted(path.iterdir())  # Sort alphabetically
        for index, child in enumerate(children):
            # Determine which prefix symbol to use (branch or final item)
            connector = "├── " if index < len(children) - 1 else "└── "
            new_prefix = prefix + ("│   " if index < len(children) - 1 else "    ")
            # Print the child
            print(prefix + connector + child.name + ("/" if child.is_dir() else ""))
            # Recurse if child is directory
            if child.is_dir():
                print_tree(child, new_prefix)

if __name__ == "__main__":
    # Change this path to the folder you want to view
    # start_path = Path(".")  # Current directory
    start_path = Path("D:/Docs/01_Projects/")
    print(f"\nDirectory tree for: {start_path.resolve()}\n")
    print_tree(start_path)
