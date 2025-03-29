# 💾 Houdini FX Cache Manager

A powerful and lightweight GUI tool to **manage, inspect, and clean up Houdini simulation caches**. Built with PySide6, this standalone desktop app helps artists quickly locate cache folders, inspect frame ranges, view metadata, and delete outdated versions of FX caches such as `.bgeo.sc`, `.vdb`, and `.abc` files.

---

## 🛠 Features

- 📂 **Scan cache directories** and auto-detect folders with FX caches
- 🔍 **Search bar and file extension filter** to quickly find what you need
- 📸 **Frame range detection** grouped by version and layer
- 🏷 **Latest version detection** with `[LATEST]` tagging
- 📑 **Detailed metadata viewer** (size, frame count, last modified date)
- 🧹 **Delete old versions** with one click — keep only the latest!
- 🗂 Option to **switch cache directories** via the UI
- ⚡ Fast and responsive even with thousands of files

---

---

## 🎬 Watch Demo

Check out the full demo on [Youtube](https://youtu.be/EcNdS6BuxVc).

---

## 📦 Supported File Types

- `.bgeo.sc`
- `.vdb`
- `.abc`

These are auto-grouped by version patterns (e.g., `fireSim_v003.1056.bgeo.sc`).

---

## 🚀 Getting Started

### 1. 📥 Install requirements:

```bash
pip install PySide6
```

### 2. ▶️ Run the tool:

```bash
python Houdini_Cache_Manager.py
```

> 💡 By default, it scans caches under `C:/Houdini_Caches`. You can change this using the **"Select Cache Folder"** button inside the app.

---

## 🖼 Interface Overview

- **Search Bar** – Filter cache folders or frame ranges
- **Extension Filter** – Only show `.bgeo.sc`, `.vdb`, or `.abc` files
- **Cache Folders Panel** – Lists valid folders with caches
- **Frame Range Panel** – Groups cache files by version/layer
- **Metadata Viewer** – Displays cache size, frame count, and modified time
- **Actions** – Refresh list, select cache, delete old versions

---

## 📂 Folder Structure Example

```
fireSim_v001.1001.bgeo.sc
fireSim_v001.1002.bgeo.sc
fireSim_v002.1001.bgeo.sc
fireSim_v002.1002.bgeo.sc
```

App detects both versions and ranges:
- `fireSim (v002).bgeo.sc (1001–1002) [LATEST]`
- `fireSim (v001).bgeo.sc (1001–1002)`

---

## 📜 License
MIT License – Free for personal and commercial use.

---

## 🔧 Future Ideas
- Add frame preview thumbnail
- Add sorting options (by size, version, date)
- Add context menu for renaming/moving

Feel free to fork and customize for your studio's cache structure!
