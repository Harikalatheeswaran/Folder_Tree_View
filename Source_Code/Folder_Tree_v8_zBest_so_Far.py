"""
Folder Tree Viewer with Rich Formatting
---------------------------------------
This script displays a colorful tree view of a selected directory in the terminal.

Features:
- Recursive folder structure display with ASCII tree formatting.
- Root folder highlighted in #FE83F8.
- Folder names colored based on depth level (cycles through colors).
- Files colored based on file extension/type (code, media, documents, etc.).
- Option to toggle between showing 📂/📄 icons and no icons (set SHOW_ICONS).
- Handles permission errors gracefully.
- Uses tkinter for directory selection GUI.
- Displays a summary of folder & file counts after printing the tree.

Dependencies:
- rich (pip install rich)

Author: Harikalatheeswaran
Version: 8
"""

import os
import tkinter as tk
from tkinter import filedialog
from rich.console import Console
from rich.text import Text
from rich import print as rprint
from pathlib import Path
from time import sleep

# === CONFIG ===
SHOW_ICONS = True  # Toggle between icons or no icons
ROOT_COLOR = "#FE83F8"  # Color for the root folder

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
    #".txt": "white",
    ".txt": "#D8D4D4",
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

import os

def get_total_size(start_path):
    """Return total size in bytes of all files under start_path."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                total_size += os.path.getsize(fp)
    return total_size
#_________________________________________________________________________________________________________________________________________________________

def gen(text: str, style: str):
    """This program is used to generate strings to print in sytl
    Eg - print_(gen("Error occured :( , failure not found!", 'bold #ff471a'))"""
    output = "[{}]{}[/{}]".format(style, text, style)
    return output

#_________________________________________________________________________________________________________________________________________________________
def human_readable_size(size_bytes):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024

#_________________________________________________________________________________________________________________________________________________________

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

#_________________________________________________________________________________________________________________________________________________________

def search_files(root_dir, keyword):
    """Search for files/folders containing the keyword and print matches with full paths."""
    console.print(f"\n[bold yellow]Searching for:[/bold yellow] [cyan]{keyword}[/cyan]\n")
    matches = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Check folders
        for d in dirnames:
            if keyword.lower() in d.lower():
                matches.append(os.path.join(dirpath, d))
        # Check files
        for f in filenames:
            if keyword.lower() in f.lower():
                matches.append(os.path.join(dirpath, f))

    if matches:
        console.print(f"[bold green]Found {len(matches)} match(es):[/bold green]\n")
        for i, match in enumerate(matches):
            #console.print(f"{i} [cyan]{os.path.basename(match)}[/cyan] → [dim]{match}[/dim]")
            console.print(f"{i+1} [cyan]{os.path.basename(match)}[/cyan] → {Path(match)}")
            print("")
        print("\n\n\n")
    else:
        console.print("[bold red]No matches found.[/bold red]")

#_________________________________________________________________________________________________________________________________________________________

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
#_________________________________________________________________________________________________________________________________________________________

if __name__ == "__main__":
    root_dir = choose_directory()
    root_name = os.path.basename(root_dir) or root_dir
    icon = "📁 " if SHOW_ICONS else ""
    root_text = Text(f"{icon}{root_name}", style=ROOT_COLOR)  # Root in pink
    console.print(root_text)
    print_tree(root_dir)

    # Summary output
    console.print("\n\n\n[bold green]Summary:[/bold green]\n")
    console.print(f"📂 [cyan]{folder_count}[/cyan] folders")
    console.print(f"📄 [magenta]{file_count}[/magenta] files")
    console.print(f"📦 Total items: [yellow]{folder_count + file_count}[/yellow]\n")
    total_size_bytes = get_total_size(root_dir)
    console.print(f"[bold cyan]Total size:[/bold cyan] {human_readable_size(total_size_bytes)} ({total_size_bytes} bytes)\n\n")

    # Search feature
    rprint("\n[bold #FEFA02]--->[/bold #FEFA02] [bold #00ffff]Enter a keyword to 🔎 search in files/folders (leave empty to skip): [/bold #00ffff]")
    keyword = input(f"🔎 KeyWord --->   ").strip()
    if keyword:
        search_files(root_dir, keyword)
    
    sleep(3.69)
    demon = """
                        ⠠⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀    ⡠⠂
                        ⠀⠘⢷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⢠⡾⠁⠀
                        ⠀⠀⢸⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⢠⣿⡇⠀⠀
                        ⠀⠀⠀⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀   ⢀⣿⣿⡇⠀⠀
                        ⠀⠀⠀⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⢀⣾⣿⣿⡇⠀⠀
                        ⠀⠀⠀⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⣠⣾⣿⣿⣿⠃⠀⠀
                        ⠀⠀⠀⢻⣿⣿⣿⣿⣷⣦⣀⠀⠀⠀⠀⣀⣤⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣦⣄⣀⠀⠀⠀⣀⣴⣾⣿⣿⣿⣿⣿⠀⠀⠀
                        ⠀⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣝⣛⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣙⣭⣥⣶⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀
                        ⠀⠀⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡏⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⢈⢿⣿⣿⣿⣿⣿⣿⣿⣿⢟⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣌⢿⣿⣿⣿⣿⣿⣿⣿⡿⢣⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⢠⣿⣦⣽⣛⣻⠿⠿⣟⣛⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣭⣛⣛⣛⣛⣻⣭⣶⣿⣧⠀⠀⠀⠀
                        ⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠀⠀⠀
                        ⠀⠀⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡸⣿⡏⢿⣿⣿⣿⡟⣼⣿⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀
                        ⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠹⣿⡈⢿⣿⠟⢰⣿⢃⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
                        ⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⠹⣷⡀⠉⢠⣿⠏⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀
                        ⠀⠀⠀⠀⣿⣿⣿⣿⣯⣍⡛⠻⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀⣿⣷⣶⣿⡟⠀⢿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠛⢋⣩⣵⣾⣿⣿⣿⡟⠀⠀⠀
                        ⠀⠀⠀⠀⣿⣿⣜⢿⣿⣿⣿⣿⣶⣶⣤⣤⣤⣉⣉⣉⣁⣀⣠⣴⣿⣿⣿⣿⣿⣤⣄⣀⣀⣀⣠⣤⣤⣴⣶⣾⣿⣿⣿⣿⡿⢋⣾⣿⣇⠀⠀⠀
                        ⠀⠀⠀⢰⣿⣿⣿⣷⣮⡝⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠛⢩⣾⣿⣿⣿⡿⣄⠀⠀
                        ⠀⠀⢰⡏⠘⢿⣿⣿⣿⣇⠀⠀⠀⠀⠉⢭⣭⣽⡟⠛⠛⠛⠋⢁⣿⣿⣿⣿⣷⡈⠉⠉⠉⠉⢭⣭⣭⠵⠀⠀⠀⠀⠀⣼⣿⣿⣿⠟⠀⣽⠀⠀
                        ⠀⠀⠀⢿⣄⠀⠻⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⣿⣿⡿⠃⢀⣾⡟⠀⠀
                        ⠀⠀⠀⠘⣿⣷⣤⣈⠛⠿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⣀⣤⣾⡿⢸⣿⣿⣿⡇⢿⣷⣤⣀⡀⠀⠀⠀⢀⣀⣤⣶⣿⡿⠟⣉⣤⣴⣿⡿⠀⠀⠀
                        ⠀⠀⠀⠀⠸⣿⣿⣿⣿⣷⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢃⣾⣿⣿⣿⣷⡈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⡿⠁⠀⠀⠀
                        ⠀⠀⠀⠀⠀⢹⣿⣭⡻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⣶⣶⡇⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⣸⣿⣿⡟⢈⣭⣟⣛⠿⠿⣿⣿⣿⠟⣩⣤⣬⣝⢿⣿⣿⣿⣿⣿⣿⣫⣥⣶⣌⠙⠿⡿⠿⠿⣛⣫⣭⣧⣄⢹⣿⣿⣇⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⣿⣿⣿⣇⣿⣿⢛⣯⣟⢿⣶⣶⣶⡇⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣷⣿⣿⣿⣿⢸⣿⣾⣿⢟⣯⣭⣝⢻⣿⣼⣿⣿⡿⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⢸⣿⣿⣿⡿⣵⣿⣿⣿⣷⢹⣿⣿⣇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣸⣿⣿⡏⣾⣿⣿⣿⣧⡹⣿⣿⣿⠇⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⢿⡿⢋⣾⣿⣿⣿⣿⠟⢈⢿⣿⣿⣷⣤⣉⠙⠿⣿⣿⣿⣿⣿⠿⠛⣉⣤⣾⣿⣿⡿⡁⠙⢿⣿⣿⣿⣿⣌⠻⡿⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⢀⣨⣶⣿⣿⡿⢟⠋⠀⠀⢸⡎⠻⣿⣿⣿⣿⣿⣶⣮⣭⣿⣯⣵⣶⣿⣿⣿⣿⡿⢟⠱⡇⠀⠀⠈⣙⡻⠿⣿⣿⣦⣄⡀⠀⠀⠀
                        ⠀⠀⠀⠀⠒⠛⠛⠉⣽⣶⣾⣿⣧⠀⠀⠈⠃⣿⣶⣶⢰⣮⡝⣛⣻⢿⣿⣿⢿⣛⡫⣵⣶⢲⣾⣿⠀⠃⠀⠀⣸⣿⣿⣿⣶⠂⠈⠉⠉⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⡄⠀⠀⠀⢿⡿⠁⠈⠛⠷⠿⠿⠿⠿⠿⠸⠿⠇⠛⠁⠀⢹⣿⠀⠀⠀⠀⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⡇⠀⠀⠀⠘⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠏⠀⠀⠀⠀⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⡇⣠⣶⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡀⠀⠀⢰⣦⢰⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⡙⠇⣰⡇⢰⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣷⢠⣷⡜⢋⣾⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣿⣇⢿⠗⣿⣿⣷⡄⣴⣶⣴⡆⣶⡆⣶⣰⣶⡄⣾⣿⣿⡞⢿⣣⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣷⣧⡻⡿⢟⣣⣛⣣⠻⣃⡻⣣⣛⣣⣛⣡⣛⡻⡿⣱⣷⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣷⣾⣿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⣿⣶⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⢿⣿⣿⣭⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣽⣿⣿⠟⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⠿⠛⠋⠉⠁⠀⠀⠀⠀⠈⠉⠙⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                    """
    rprint(gen(demon.center(99, "*"), "bold #6BFF21")) #FF0000 #6BFF21



#_________________________________________________________________________________________________________________________________________________________
