import os
import tkinter as tk
from tkinter import filedialog
from rich.console import Console
from rich.tree import Tree
from rich.text import Text

# 🎨 Color palette for top-level branches
BRANCH_COLORS = [
    "bold bright_magenta",
    "bold bright_cyan",
    "bold bright_green",
    "bold bright_yellow",
    "bold bright_blue",
    "bold bright_red",
]

console = Console()

def select_folder():
    """
    Opens a Tkinter dialog for the user to select a folder.
    Defaults to current working directory if no folder is chosen.
    """
    root = tk.Tk()
    root.withdraw()  # Hide main Tkinter window
    console.print("\n[bold #FEFA02]---> Press Enter to select the folder you want to visualize[/]", end="")
    input()
    selected_dir = filedialog.askdirectory()
    return selected_dir if selected_dir else os.getcwd()

def add_branch(tree, path, branch_color):
    """
    Recursively adds folders and files to the Rich tree.
    
    Args:
        tree (Tree): The Rich Tree object to append items to.
        path (str): The current directory path being explored.
        branch_color (str): The Rich style for this branch.
    """
    try:
        items = sorted(os.listdir(path))  # Sort alphabetically
    except PermissionError:
        return  # Skip folders we don't have permission for

    for item in items:
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            # 📂 Add folder in branch color
            folder_node = tree.add(Text(f"📂 {item}", style=branch_color))
            add_branch(folder_node, full_path, branch_color)  # Recurse deeper
        else:
            # 📄 Add file with dimmed branch color
            tree.add(Text(f"📄 {item}", style=f"{branch_color} dim"))

def build_tree(base_path):
    """
    Builds and displays the folder structure as a Rich Tree
    with unique colors for each top-level branch.
    """
    # 🌳 Root node in bold purple
    tree = Tree(Text(f"📁 {os.path.basename(base_path)}", style="bold purple"))

    try:
        items = sorted(os.listdir(base_path))
    except PermissionError:
        console.print("[red]Error: Cannot access base folder[/]")
        return

    color_index = 0  # Index to cycle through BRANCH_COLORS

    for item in items:
        full_path = os.path.join(base_path, item)
        if os.path.isdir(full_path):
            # Assign unique color to this top-level branch
            branch_color = BRANCH_COLORS[color_index % len(BRANCH_COLORS)]
            color_index += 1

            # 📂 Add colored branch and recurse
            branch_node = tree.add(Text(f"📂 {item}", style=branch_color))
            add_branch(branch_node, full_path, branch_color)
        else:
            # 📄 Files directly in root are plain white
            tree.add(Text(f"📄 {item}", style="white"))

    console.print(tree)

if __name__ == "__main__":
    folder_path = select_folder()
    build_tree(folder_path)
