import sys
import os
import re
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QPushButton, QFileDialog, QLabel, QLineEdit, QComboBox
from PySide6.QtCore import QDateTime

# Default cache directory (change this if needed)
CACHE_DIR = "C:/Houdini_Caches"

class FXCacheManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FX Cache Manager")
        self.setGeometry(100, 100, 600, 600)

        layout = QVBoxLayout()

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search caches or folders...")
        layout.addWidget(self.search_bar)

        # Filter Dropdown
        self.filter_dropdown = QComboBox()
        self.filter_dropdown.addItems(["All", ".bgeo.sc", ".vdb", ".abc"])
        layout.addWidget(self.filter_dropdown)

        # Cache Folder Selection
        self.folder_list = QListWidget()
        layout.addWidget(QLabel("Cache Folders:"))
        layout.addWidget(self.folder_list)

        # Cache Files (Grouped by Version & Layer)
        self.cache_list = QListWidget()
        layout.addWidget(QLabel("Frame Ranges:"))
        layout.addWidget(self.cache_list)

        # Metadata Display
        self.metadata_label = QLabel("Cache Metadata: \nSize: -\nFrames: -\nModified: -")
        layout.addWidget(self.metadata_label)
        
        # Buttons
        self.load_button = QPushButton("Select Cache Folder")
        self.refresh_button = QPushButton("Refresh List")
        self.select_button = QPushButton("Select Cache")
        self.delete_old_versions_button = QPushButton("Delete Old Versions")

        layout.addWidget(self.load_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.select_button)
        layout.addWidget(self.delete_old_versions_button)

        self.setLayout(layout)

        # Button Connections
        self.load_button.clicked.connect(self.select_cache_folder)
        self.refresh_button.clicked.connect(self.list_existing_folders)
        self.select_button.clicked.connect(self.select_cache)
        self.delete_old_versions_button.clicked.connect(self.delete_old_versions)
        self.folder_list.itemClicked.connect(self.list_cache_files)
        self.cache_list.itemClicked.connect(self.display_cache_metadata)
        self.search_bar.textChanged.connect(self.filter_results)
        self.filter_dropdown.currentTextChanged.connect(self.list_existing_folders)

        # Load folders from default directory
        self.list_existing_folders()

    def list_existing_folders(self):
        """Lists only the deepest cache folders containing selected file types."""
        self.folder_list.clear()
        selected_ext = self.filter_dropdown.currentText()
        cache_folders = set()
        
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        
        for root, dirs, files in os.walk(CACHE_DIR):
            if any(file.endswith(selected_ext) or selected_ext == "All" for file in files):
                cache_folders.add(root.replace(CACHE_DIR, "").strip("\\"))
        
        for folder in sorted(cache_folders):
            self.folder_list.addItem(folder)

    def list_cache_files(self, item):
        """Lists frame ranges from the deepest cache folder."""
        selected_folder = os.path.join(CACHE_DIR, item.text())
        self.cache_list.clear()
        frame_sequences = self.group_frames_by_range(selected_folder)
        for seq in frame_sequences:
            self.cache_list.addItem(seq)

    def group_frames_by_range(self, folder):
        """Groups frames into frame ranges and organizes them by version & layer."""
        frame_dict = {}
        latest_versions = {}
        
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith((".bgeo.sc", ".vdb", ".abc")):
                    match = re.match(r"(.+?)_(v\d+)\.(\d+)\.(bgeo\.sc|vdb|abc)$", file)
                    if match:
                        base_name, version, frame, ext = match.groups()
                        frame = int(frame)
                        key = f"{base_name} ({version}).{ext}"
                        if key not in frame_dict:
                            frame_dict[key] = []
                        frame_dict[key].append(frame)
                        latest_versions[base_name] = max(latest_versions.get(base_name, version), version)
        
        frame_ranges = []
        for key, frames in frame_dict.items():
            frames.sort()
            base_name = key.split(" (")[0]
            latest_tag = " [LATEST]" if latest_versions[base_name] in key else ""
            frame_ranges.append(f"{key} ({frames[0]}-{frames[-1]}){latest_tag}")
        return frame_ranges

    def delete_old_versions(self):
        """Deletes old versions of caches, keeping only the latest version."""
        selected_folder = self.folder_list.currentItem()
        if not selected_folder:
            return

        cache_folder = os.path.join(CACHE_DIR, selected_folder.text())
        latest_versions = {}

        for root, _, files in os.walk(cache_folder):
            for file in files:
                match = re.match(r"(.+?)_(v\d+)\.(\d+)\.(bgeo\.sc|vdb|abc)$", file)
                if match:
                    base_name, version, _, _ = match.groups()
                    latest_versions[base_name] = max(latest_versions.get(base_name, version), version)

        for root, _, files in os.walk(cache_folder):
            for file in files:
                match = re.match(r"(.+?)_(v\d+)\.(\d+)\.(bgeo\.sc|vdb|abc)$", file)
                if match:
                    base_name, version, _, _ = match.groups()
                    if version != latest_versions[base_name]:
                        os.remove(os.path.join(root, file))

        self.list_cache_files(selected_folder)
    
    def display_cache_metadata(self, item):
        """Displays metadata for the selected cache."""
        selected_folder = self.folder_list.currentItem()
        if not selected_folder:
            return
        
        cache_folder = os.path.join(CACHE_DIR, selected_folder.text())
        cache_name = item.text().split(" (")[0]  # Extract base name
        total_size = 0
        frame_count = 0
        last_modified = None

        for root, _, files in os.walk(cache_folder):
            for file in files:
                if file.startswith(cache_name) and file.endswith((".bgeo.sc", ".vdb", ".abc")):
                    file_path = os.path.join(root, file)
                    total_size += os.path.getsize(file_path)
                    frame_count += 1
                    mod_time = os.path.getmtime(file_path)
                    if last_modified is None or mod_time > last_modified:
                        last_modified = mod_time

        size_mb = total_size / (1024 * 1024)  # Convert to MB
        mod_time_str = QDateTime.fromSecsSinceEpoch(int(last_modified)).toString("yyyy-MM-dd HH:mm:ss") if last_modified else "-"

        self.metadata_label.setText(f"Cache Metadata:\nSize: {size_mb:.2f} MB\nFrames: {frame_count}\nModified: {mod_time_str}")

    def select_cache_folder(self):
        """Allows user to select a different cache folder."""
        global CACHE_DIR
        folder = QFileDialog.getExistingDirectory(self, "Select Cache Folder", CACHE_DIR)
        if folder:
            CACHE_DIR = folder
            self.list_existing_folders()
            print(f"Cache folder set to: {CACHE_DIR}")

    def select_cache(self):
        """Prints the selected cache folder and frame range."""
        selected_folder = self.folder_list.currentItem()
        selected_cache = self.cache_list.currentItem()
        if selected_folder and selected_cache:
            cache_path = os.path.join(CACHE_DIR, selected_folder.text(), selected_cache.text())
            print(f"Selected Cache: {cache_path}")

    def filter_results(self):
        """Filters cache list and folder list based on search query."""
        search_text = self.search_bar.text().lower()
        for i in range(self.folder_list.count()):
            item = self.folder_list.item(i)
            item.setHidden(search_text not in item.text().lower())
        for i in range(self.cache_list.count()):
            item = self.cache_list.item(i)
            item.setHidden(search_text not in item.text().lower())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FXCacheManager()
    window.show()
    sys.exit(app.exec())
