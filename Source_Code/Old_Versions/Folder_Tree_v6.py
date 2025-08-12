import os
import tkinter as tk
from tkinter import filedialog
from rich.console import Console
from rich.text import Text

"""
This version had uniform color fro each depth.
"""


# === CONFIG ===
SHOW_ICONS = False  # Toggle between icons or no icons

# Define colors for each depth level (cycles if deeper)
DEPTH_COLORS = [
    "bold purple",
    "bright_magenta",
    "bright_cyan",
    "bright_green",
    "bright_yellow",
    "bright_blue"
]

console = Console()

def choose_directory():
    """Prompt user to choose a folder, default to current dir if none selected."""
    root = tk.Tk()
    root.withdraw()
    console.print("\n[bold #FEFA02]--->[/bold #FEFA02] [bold #00ffff]Press Enter to select the folder to display tree view...[/bold #00ffff]")
    input()
    selected_dir = filedialog.askdirectory()
    return selected_dir if selected_dir else os.getcwd()

def print_tree(dir_path, prefix="", depth=0):
    """Recursively print the directory tree with depth-based colors."""
    try:
        items = sorted(os.scandir(dir_path), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        console.print(prefix + "[red][Access Denied][/red]")
        return

    pointers = ['├──'] * (len(items) - 1) + ['└──']
    folder_color = DEPTH_COLORS[depth % len(DEPTH_COLORS)]

    for pointer, entry in zip(pointers, items):
        icon = "📂 " if entry.is_dir() else "📄 " if SHOW_ICONS else ""
        #style = folder_color if entry.is_dir() else "white" # <--- Keep this if you want to print in white.
        style = folder_color if entry.is_dir() else None

        text = Text(f"{pointer} {icon}{entry.name}", style=style) # type: ignore
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
