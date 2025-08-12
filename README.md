# 📂 🌴 Folder Tree Viewer with Rich Formatting

A Python script to display a **colorful, organized tree view** of any folder in your terminal — complete with **icons, depth-based coloring, file-type highlighting, and a summary report**.

---

## ✨ Features

- 🎨 **Beautiful colored output** using [Rich](https://github.com/Textualize/rich)
- 📁 **Root folder highlighted** in pink (`#FE83F8`)
- 🌳 **Depth-based coloring** for folders (same level = same color)
- 📄 **File-type based coloring** (code, docs, media, logs, etc.)
- 📑 **Optional folder & file icons** — toggle with `SHOW_ICONS`
- 🚫 **Permission error handling**
- 🖱️ **Simple GUI folder picker** (via `tkinter`)
- 📊 **Summary section** after tree view:
  - Total folders
  - Total files
  - Total items
  - **Total size** (bytes + human-readable)



---
## ⚙️ Configuration
You can customize the script’s behavior by editing the variables in the code:

| Variable           | Type | Description                                      |
| ------------------ | ---- | ------------------------------------------------ |
| `SHOW_ICONS`       | bool | Toggle file/folder icons (`True` or `False`)     |
| `ROOT_COLOR`       | str  | Hex or Rich-compatible color for the root folder |
| `DEPTH_COLORS`     | list | Colors for folder levels (cycled per depth)      |
| `FILE_TYPE_COLORS` | dict | Mapping of file extensions to colors             |

---
## 📦 Installation
```bash
# Clone this repo or copy the script
git clone https://github.com/yourusername/folder-tree-viewer.git

# Install dependencies
pip install rich
Note: tkinter is included in most Python installations.
On some Linux distros, you may need to install it via your package manager.
```
---
## 🚀 Usage

```bash
python folder_tree_viewer.py
```
---
## 🖌 Customization
### 🎨 Change Folder Depth Colors
Edit the DEPTH_COLORS list to define colors for different levels:
```python
DEPTH_COLORS = ["cyan", "green", "yellow", "magenta", "blue"]
```

### 📄 Add File Type Colors
You can map file extensions to specific colors:
```python
FILE_TYPE_COLORS = {
    ".py": "bright_green",
    ".txt": "yellow",
    ".md": "cyan",
    ".json": "magenta",
    ".log": "red",
}
```

### 🎯 Highlight Root Folder
The root folder color can be changed via:
```python
ROOT_COLOR = "#FE83F8"
```


### 🎯 Highlight Root Folder
Change root folder color:

```python
ROOT_COLOR = "#FE83F8"
```

### 🔕 Disable Icons
Disable icons for a simpler text-only output:

```python
SHOW_ICONS = False
```

---

## 📊 Output Summary

At the end of the output, you will see:

```plaintext
📁 MyProjects
├── 📂 Scripts
│   ├── 📄 script1.py
│   └── 📄 script2.sh
└── 📂 Docs
    ├── 📄 notes.txt
    └── 📄 guide.pdf

Summary:

📂  3 folders  
📄  4 files  
📦  Total items: 7  
💾  Total size: 12.34 MB (12942384 bytes)
```
---

## 📜 LICENSE
```
License: MIT © 2025 Harikalatheeswaran
See LICENSE file for details.
```
