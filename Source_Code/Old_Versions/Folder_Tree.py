import json
from pathlib import Path
from typing import Dict, Union
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


def build_folder_dict(folder_path: str) -> Dict[str, Union[list, dict]]:
    """
    Recursively builds a nested dictionary representing the folder structure.

    Each folder is represented as:
    {
        "files": [...],
        "subfolders": {
            "subfolder_name": { ... same structure ... }
        }
    }

    This version FIXES the earlier limitation where "subfolders" was always an empty dictionary.
    Now, each folder actually contains its subfolders as nested dictionaries.
    This ensures no folder is skipped and the structure matches the real filesystem hierarchy.

    Args:
        folder_path (str): Path to the folder you want to scan.

    Returns:
        dict: Nested dictionary with 'files' and 'subfolders'.
    """
    folder_dict = {"files": [], "subfolders": {}}
    path_obj = Path(folder_path)

    try:
        for item in path_obj.iterdir():
            if item.is_file():
                try:
                    # Check if file is readable (light read)
                    with item.open('rb') as f:
                        f.read(1024)
                    folder_dict["files"].append(item.name)
                except (PermissionError, IOError):
                    # Skip files we cannot access
                    continue
            elif item.is_dir():
                # Recursively build structure for subfolder
                folder_dict["subfolders"][item.name] = build_folder_dict(item) # type: ignore
    except (PermissionError, OSError):
        # Skip folders we cannot access
        pass

    return folder_dict


def print_ascii_tree_from_dict(
    folder_dict: Dict[str, Union[list, dict]],
    folder_name: str = ".",
    prefix: str = ""
) -> None:
    """
    Recursively prints the folder tree with correct indentation and no missing folders.

    FIXED VERSION:
    - Uses the real 'subfolders' dictionary instead of string-based guessing.
    - Ensures every subfolder is printed exactly once, at the correct depth.
    - Produces a clean, professional ASCII tree similar to the 'tree' command.

    Args:
        folder_dict: Dictionary returned by build_folder_dict().
        folder_name: Current folder name (root is ".").
        prefix: Indentation string for proper alignment.
    """
    print_(gen(f"{prefix}└── {folder_name}/", "bold blue"))

    files = sorted(folder_dict.get("files", []))
    subfolders = sorted(folder_dict.get("subfolders", {}).items()) # type: ignore

    # Print files in this folder
    for i, file in enumerate(files):
        connector = "└──" if i == len(files) - 1 and not subfolders else "├──"
        print_(gen(f"{prefix}    {connector} {file}", "green"))

    # Recursively print subfolders
    for i, (subfolder_name, subfolder_content) in enumerate(subfolders):
        is_last = i == len(subfolders) - 1
        new_prefix = prefix + ("    " if is_last else "    ")
        print_ascii_tree_from_dict(subfolder_content, subfolder_name, new_prefix)


def print_ascii_tree_from_json(json_path: str) -> None:
    """
    Prints an ASCII tree of the folder structure from a JSON file.

    Reads a JSON file containing a folder dictionary (from build_folder_dict) and prints it in an ASCII tree format.

    Args:
        json_path (str): Path to the JSON file with the folder structure.

    Returns:
        None
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            folder_dict = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError) as e:
        print_(gen(f"Error: Can't read JSON file {json_path}: {e}", "bold red"))
        return

    # Important: JSON loses Path objects, so we print from nested structure
    print_ascii_tree_from_dict(folder_dict)


if __name__ == "__main__":
    # Example usage: scan a folder and print its structure
    folder_path = "D:/Docs/01_Projects/"  # Change this to your target folder

    # Step 1: Build folder dictionary
    result = build_folder_dict(folder_path)

    # Step 2: Print JSON output for debugging
    print_(gen("\nJSON Output:", "bold"))
    print(json.dumps(result, indent=2))

    # Step 3: Print folder structure as ASCII tree
    print_(gen("\nFolder Structure as ASCII Tree:", "bold"))
    print_ascii_tree_from_dict(result)

    # Step 4: Save the folder structure to a JSON file
    json_path = "folder_structure.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

    # Step 5: Load from JSON and print again
    print_(gen("\nFolder Structure from JSON File:", "bold"))
    print_ascii_tree_from_json(json_path)
