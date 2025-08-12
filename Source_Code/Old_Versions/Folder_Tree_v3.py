import json
from pathlib import Path
from typing import Dict, Union, List, Any
from rich import print as print_

# Why we use the typing module:
# The typing module helps us tell Python what kinds of data (like strings, lists, or dictionaries) a function expects
# or returns. This makes our code clearer, easier to understand, and helps catch mistakes early, especially when
# working with complex data like dictionaries that hold lists or other dictionaries.
# Think of it like giving your future self (and other developers) a clear roadmap for how the data is structured.

# About Dict and Union:
# - Dict[str, Union[list, dict]]: This means a dictionary where keys are strings, and values can be either a list
#   (like a list of file names) or another dictionary (for subfolders). Union[list, dict] allows the value to be one
#   of these types, making our code flexible but clear.
# - This is especially helpful when working with folder trees, where each folder might have files (list) and also
#   more folders inside (dict).


def gen(text: str, style: str) -> str:
    """
    Generates a styled string for printing with rich.

    This function wraps text in a style tag for colorful output using the rich library. For example, you can make
    text bold and red or blue and italic. It's like adding decorations to text to make it stand out.

    Args:
        text (str): The text you want to style.
        style (str): The style to apply (e.g., 'bold red', 'blue', 'cyan').

    Returns:
        str: The text wrapped in rich style tags, like '[bold red]text[/bold red]'.

    Example:
        >>> print_(gen("Hello!", "bold blue"))
        [bold blue]Hello![/bold blue]
    """
    return f"[{style}]{text}[/{style}]"


def build_folder_dict(folder_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Recursively builds a nested dictionary representing the folder structure.

    Each folder is represented as:
    {
        "files": [...],
        "subfolders": {
            "subfolder_name": { ... same structure ... }
        }
    }

    This function looks through a folder and all its subfolders to create a dictionary. Each key in the dictionary
    is a folder path (relative to the starting folder), and its value is another dictionary that lists files and
    subfolders. It only includes files we can read and skips anything that causes errors.

    Args:
        folder_path (str | Path): The path to the folder you want to scan (e.g., "C:/MyFolder").

    Returns:
        dict: Nested dictionary with 'files' and 'subfolders'.

    Example:
        >>> result = build_folder_dict("D:/Docs/")
        >>> print(json.dumps(result, indent=2))
    """
    path_obj = Path(folder_path)

    # Prepare structure for this folder
    folder_dict: Dict[str, Any] = {"files": [], "subfolders": {}}

    # Defensive: ensure path exists and is a directory
    try:
        if not path_obj.exists() or not path_obj.is_dir():
            return folder_dict
    except (PermissionError, OSError):
        return folder_dict

    try:
        for item in sorted(path_obj.iterdir(), key=lambda p: p.name.lower()):
            # Skip symlinks to avoid possible recursion loops
            if item.is_symlink():
                continue

            if item.is_file():
                try:
                    # Light read to ensure file is accessible (don't load entire file)
                    with item.open("rb") as f:
                        f.read(1024)
                    folder_dict["files"].append(item.name)
                except (PermissionError, IOError, OSError):
                    # Skip unreadable files
                    continue

            elif item.is_dir():
                # Recursively build nested structure for subfolder
                folder_dict["subfolders"][item.name] = build_folder_dict(item)

    except (PermissionError, OSError):
        # Skip folders we cannot access
        pass

    return folder_dict


def print_ascii_tree_from_dict(
    folder_dict: Dict[str, Any],
    folder_name: str = ".",
    prefix: str = ""
) -> None:
    """
    Recursively prints the folder tree with correct indentation and colors.

    FIXED & ENHANCED:
    - Uses the real nested 'subfolders' mapping produced by build_folder_dict().
    - Prints directories and files in sorted order.
    - Uses 'gen' for colors:
        - directories: bold blue
        - files: green
    - Uses ASCII connectors: '│', '├──', '└──' for a clean tree look.

    Args:
        folder_dict: Nested dictionary returned by build_folder_dict().
        folder_name: Display name for the current folder (root defaults to ".").
        prefix: Prefix string used to draw vertical lines and spacing.
    """
    # Print the current folder name (root or subfolder)
    # Folder line uses no connector for the top-level call (cleaner output)
    if prefix == "":
        print_(gen(f"{folder_name}/", "bold blue"))
    else:
        # When prefix is non-empty we are inside recursion and prefix contains vertical bars/spacing
        # connector is already included in previous call when printing the item line
        print_(gen(f"{prefix}{folder_name}/", "bold blue"))

    # Build ordered entries: directories first, then files (both sorted)
    subfolders_items = sorted(folder_dict.get("subfolders", {}).items(), key=lambda kv: kv[0].lower())
    files_items = sorted(folder_dict.get("files", []), key=lambda s: s.lower())

    entries: List[Any] = []
    for name, content in subfolders_items:
        entries.append((name, True, content))
    for name in files_items:
        entries.append((name, False, None))

    # Print each entry with appropriate connector, recurse for directories
    for idx, (name, is_dir, content) in enumerate(entries):
        is_last = idx == (len(entries) - 1)
        connector = "└── " if is_last else "├── "
        line = prefix + connector + (name + "/" if is_dir else name)

        # Use colors via gen: folders bold blue, files green
        if is_dir:
            print_(gen(line, "bold blue"))
            # New prefix extends previous prefix: use vertical bar for non-last, spaces for last
            new_prefix = prefix + ("    " if is_last else "│   ")
            # Recurse into the subfolder's nested dict
            print_ascii_tree_from_dict(content, "", new_prefix)
        else:
            print_(gen(line, "green"))


def print_ascii_tree_from_json(json_path: str) -> None:
    """
    Prints an ASCII tree of the folder structure from a JSON file.

    This function reads a JSON file that contains a folder dictionary (like the one from build_folder_dict)
    and prints it as an ASCII tree. Folders are in bold blue, files in green, and subfolders in cyan.

    Args:
        json_path (str): Path to the JSON file with the folder structure.

    Returns:
        None: Just prints the tree to the console.

    Example:
        >>> print_ascii_tree_from_json("folder_structure.json")
    """
    # Try to read the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            folder_dict = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        # If we can't read the JSON file, print an error in bold red
        print_(gen(f"Error: Can't read JSON file {json_path}: {e}", "bold red"))
        return

    # Use the nested-structure printer to render the tree
    print_ascii_tree_from_dict(folder_dict)


if __name__ == "__main__":
    # Example usage: scan a folder and print its structure
    folder_path = "D:/Docs/01_Projects/"  # Change this to your target folder

    # Build a nested folder dictionary (files + subfolders)
    result = build_folder_dict(folder_path)

    # Print the dictionary as JSON for debugging
    print_(gen("\nJSON Output:", "bold"))
    print(json.dumps(result, indent=2))

    # Print the dictionary as an ASCII tree (colored)
    print_(gen("\nFolder Structure as ASCII Tree:", "bold"))
    print_ascii_tree_from_dict(result)

    # Save the dictionary to a JSON file and print it from file to confirm load/save
    json_path = "folder_structure.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

    print_(gen("\nFolder Structure from JSON File:", "bold"))
    print_ascii_tree_from_json(json_path)
