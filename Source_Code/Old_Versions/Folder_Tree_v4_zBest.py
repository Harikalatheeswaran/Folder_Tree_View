"""
Folder tree visualizer
- User selects a folder via a Tkinter dialog (press Enter to open).
- If user cancels, defaults to the current working directory.
- Uses rich.Tree for a beautiful, colored tree view.
- Keeps comments concise and informative.
"""

import os
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.tree import Tree
from rich.text import Text

# -------------------------
# Console / helper (rich)
# -------------------------
console = Console()

def gen(text: str, style: str) -> Text:
    """
    Returns a rich.Text object with the given style.
    Use styles like: 'bold blue', 'bold magenta', 'green', or hex colors 'bold #00ffff'.
    This keeps color usage centralized so all print calls are consistent.
    """
    return Text(text, style=style)


# -------------------------
# Tree builder
# -------------------------
def build_tree(directory: Path, rich_tree: Tree, depth: int = 0) -> None:
    """
    Recursively builds the given rich_tree from the filesystem directory.

    Args:
        directory: Path object for the directory to scan.
        rich_tree: A rich.Tree node to attach children to.
        depth: Current depth (0 for root). Used to choose styling if needed.
    """
    try:
        # Sort: directories first, then files; case-insensitive order
        entries = sorted(directory.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except PermissionError:
        # If we can't read this directory, add a red warning node and return
        rich_tree.add(gen("[Permission Denied]", "bold red"))
        return
    except OSError:
        # Generic OS error (e.g., path disappeared), skip gracefully
        rich_tree.add(gen("[Error accessing folder]", "bold red"))
        return

    for entry in entries:
        # Avoid following symlinks (prevent loops)
        try:
            if entry.is_symlink():
                # Show symlink name (colored as file) but do not recurse
                rich_tree.add(gen(f"{entry.name} -> (symlink)", "green"))
                continue
        except OSError:
            # If is_symlink check fails, skip entry
            continue

        if entry.is_dir():
            # Folder color logic:
            # - root (depth == 0): bold magenta (stands out)
            # - nested folders (depth >= 1): bold blue (consistent and readable)
            style = "bold magenta" if depth == 0 else "bold blue"
            # Add folder node (Text object ensures color is retained)
            branch = rich_tree.add(gen(f"{entry.name}/", style))
            # Recurse into subfolder with increased depth
            build_tree(entry, branch, depth + 1)
        else:
            # Files are green for easy scanning
            rich_tree.add(gen(entry.name, "green"))


# -------------------------
# Main CLI + folder picker
# -------------------------
def main(initial_dir: Optional[str] = None) -> None:
    """
    Prompt user to select a folder (Tkinter). If none selected, use current working directory.
    Build and display a colored tree view using rich.
    """
    # Hide Tk root window — we only want the file dialog
    root = tk.Tk()
    root.withdraw()

    # Prompt and pause so user can prepare for the dialog
    console.print(gen("---> ", "bold #FEFA02"), gen("Press Enter to select the folder you want to visualize (Cancel = current folder).", "bold #00ffff"))
    input()  # Wait for Enter

    # Show folder dialog
    selected_dir = filedialog.askdirectory(initialdir=initial_dir) if initial_dir else filedialog.askdirectory()
    if not selected_dir:
        selected_dir = os.getcwd()

    directory = Path(selected_dir)

    # Build rich tree with colored root
    root_label = gen(f"{directory.name}/", "bold magenta")
    tree = Tree(root_label)

    build_tree(directory, tree, depth=0)

    # Print header and tree
    console.print()
    console.print(gen("📂 Directory Structure:", "bold green"))
    console.print(gen(str(directory.resolve()), "bold cyan"))
    console.print()
    console.print(tree)


if __name__ == "__main__":
    main()
