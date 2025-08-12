# """
# Folder Tree Viewer with Rich Formatting
# ---------------------------------------
# This script displays a colorful tree view of a selected directory in the terminal.

# Features:
# - Recursive folder structure display with ASCII tree formatting.
# - Folder names colored based on depth level (cycles through colors).
# - Files colored based on file extension/type (code, media, documents, etc.).
# - Option to toggle between showing 📂/📄 icons and no icons (set SHOW_ICONS).
# - Handles permission errors gracefully.
# - Uses tkinter for directory selection GUI.

# Dependencies:
# - rich (pip install rich)

# Author: [Your Name]
# Version: 2.0
# """

# import os
# import tkinter as tk
# from tkinter import filedialog
# from rich.console import Console
# from rich.text import Text

# # === CONFIG ===
# SHOW_ICONS = True  # Toggle between icons or no icons

# # Define colors for folders by depth
# """
# DEPTH_COLORS = [
#     "bold purple",
#     "bright_magenta",
#     "bright_cyan",
#     "bright_green",
#     "bright_yellow",
#     "bright_blue"
# ]
# """
# DEPTH_COLORS = [
#     "bold #22FFC4",
#     "bright_magenta",
#     "bright_cyan",
#     "bright_green",
#     "bright_yellow",
#     "bright_blue"
# ]


# # File type color mapping
# FILE_TYPE_COLORS = {
#     # Code
#     ".py": "bright_green",
#     ".js": "bright_yellow",
#     ".html": "bright_magenta",
#     ".css": "cyan",
#     ".java": "bright_blue",
#     ".c": "blue",
#     ".cpp": "blue",
#     ".sh": "green",
#     # Documents
#     ".txt": "white",
#     ".md": "bright_white",
#     ".pdf": "red",
#     ".doc": "bright_blue",
#     ".docx": "bright_blue",
#     ".xls": "bright_green",
#     ".xlsx": "bright_green",
#     # Images
#     ".png": "magenta",
#     ".jpg": "bright_magenta",
#     ".jpeg": "bright_magenta",
#     ".gif": "bright_yellow",
#     # Logs
#     ".log": "yellow",
#     ".csv": "cyan"
# }

# console = Console()

# def choose_directory():
#     """Prompt user to choose a folder, default to current dir if none selected."""
#     root = tk.Tk()
#     root.withdraw()
#     console.print("\n[bold #FEFA02]--->[/bold #FEFA02] [bold #00ffff]Press Enter to select the folder to display tree view...[/bold #00ffff]")
#     input()
#     selected_dir = filedialog.askdirectory()
#     return selected_dir if selected_dir else os.getcwd()

# def get_file_color(filename):
#     """Return color based on file extension, default to white."""
#     ext = os.path.splitext(filename)[1].lower()
#     return FILE_TYPE_COLORS.get(ext, "white")

# def print_tree(dir_path, prefix="", depth=0):
#     """Recursively print the directory tree with depth-based folder and file coloring."""
#     try:
#         items = sorted(os.scandir(dir_path), key=lambda e: (not e.is_dir(), e.name.lower()))
#     except PermissionError:
#         console.print(prefix + "[red][Access Denied][/red]")
#         return

#     pointers = ['├──'] * (len(items) - 1) + ['└──']

#     for pointer, entry in zip(pointers, items):
#         if entry.is_dir():
#             style = DEPTH_COLORS[depth % len(DEPTH_COLORS)]
#         else:
#             style = get_file_color(entry.name)

#         icon = "📂 " if entry.is_dir() else "📄 " if SHOW_ICONS else ""
#         text = Text(f"{pointer} {icon}{entry.name}", style=style)
#         console.print(prefix, text, sep="")

#         if entry.is_dir():
#             extension = "│   " if pointer == "├──" else "    "
#             print_tree(entry.path, prefix + extension, depth + 1)

# if __name__ == "__main__":
#     root_dir = choose_directory()
#     root_name = os.path.basename(root_dir) or root_dir
#     icon = "📁 " if SHOW_ICONS else ""
#     root_text = Text(f"{icon}{root_name}", style=DEPTH_COLORS[0])
#     console.print(root_text)
#     print_tree(root_dir)



"""
Folder Tree Viewer with Rich Formatting
---------------------------------------
This script displays a colorful tree view of a selected directory in the terminal.

Features:
- Recursive folder structure display with ASCII tree formatting.
- Folder names colored based on depth level (cycles through colors).
- Files colored based on file extension/type (code, media, documents, etc.).
- Option to toggle between showing 📂/📄 icons and no icons (set SHOW_ICONS).
- Handles permission errors gracefully.
- Uses tkinter for directory selection GUI.
- Displays a summary of folder & file counts after printing the tree.

Dependencies:
- rich (pip install rich)

Author: [Your Name]
Version: 2.1
"""

import os
import tkinter as tk
from tkinter import filedialog
from rich.console import Console
from rich.text import Text

# === CONFIG ===
SHOW_ICONS = True  # Toggle between icons or no icons

# Define colors for folders by depth
DEPTH_COLORS = [
    "bold #22FFC4",
    "bright_magenta",
    "bright_cyan",
    "bright_green",
    "bright_yellow",
    "bright_blue"
]

# File type color mapping
FILE_TYPE_COLORS = {
    # Code
    ".py": "bright_green",
    ".js": "bright_yellow",
    ".html": "bright_magenta",
    ".css": "cyan",
    ".java": "bright_blue",
    ".c": "blue",
    ".cpp": "blue",
    ".sh": "green",
    # Documents
    ".txt": "white",
    ".md": "bright_white",
    ".pdf": "red",
    ".doc": "bright_blue",
    ".docx": "bright_blue",
    ".xls": "bright_green",
    ".xlsx": "bright_green",
    # Images
    ".png": "magenta",
    ".jpg": "bright_magenta",
    ".jpeg": "bright_magenta",
    ".gif": "bright_yellow",
    # Logs
    ".log": "yellow",
    ".csv": "cyan"
}

console = Console()

# Counters
folder_count = 0
file_count = 0

def choose_directory():
    """Prompt user to choose a folder, default to current dir if none selected."""
    root = tk.Tk()
    root.withdraw()
    console.print("\n[bold #FEFA02]--->[/bold #FEFA02] [bold #00ffff]Press Enter to select the folder to display tree view...[/bold #00ffff]")
    input()
    selected_dir = filedialog.askdirectory()
    return selected_dir if selected_dir else os.getcwd()

def get_file_color(filename):
    """Return color based on file extension, default to white."""
    ext = os.path.splitext(filename)[1].lower()
    return FILE_TYPE_COLORS.get(ext, "white")

def print_tree(dir_path, prefix="", depth=0):
    """Recursively print the directory tree with depth-based folder and file coloring."""
    global folder_count, file_count

    try:
        items = sorted(os.scandir(dir_path), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        console.print(prefix + "[red][Access Denied][/red]")
        return

    pointers = ['├──'] * (len(items) - 1) + ['└──']

    for pointer, entry in zip(pointers, items):
        if entry.is_dir():
            folder_count += 1
            style = DEPTH_COLORS[depth % len(DEPTH_COLORS)]
        else:
            file_count += 1
            style = get_file_color(entry.name)

        icon = "📂 " if entry.is_dir() else "📄 " if SHOW_ICONS else ""
        text = Text(f"{pointer} {icon}{entry.name}", style=style)
        console.print(prefix, text, sep="")

        if entry.is_dir():
            extension = "│   " if pointer == "├──" else "    "
            print_tree(entry.path, prefix + extension, depth + 1)

if __name__ == "__main__":
    root_dir = choose_directory()
    root_name = os.path.basename(root_dir) or root_dir
    icon = "📁 " if SHOW_ICONS else ""
    root_text = Text(f"{icon}{root_name}", style=DEPTH_COLORS[0])
    console.print(root_text)
    print_tree(root_dir)

    # Summary output
    console.print("\n\n\n[bold green]Summary:[/bold green]\n")
    console.print(f"📂 [cyan]{folder_count}[/cyan] folders")
    console.print(f"📄 [magenta]{file_count}[/magenta] files")
    console.print(f"📦 Total items: [yellow]{folder_count + file_count}[/yellow]\n\n\n")
