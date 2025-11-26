from krita import DockWidget, DockWidgetFactory, Krita
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QListWidget, QListWidgetItem, QLabel,
    QScrollArea, QGridLayout, QComboBox, QLineEdit,
    QSlider, QCheckBox, QGroupBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap


class MultiPageComicsDocker(DockWidget):
    """Main docker panel for Comic Creator"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Comic Creator")

        # Main widget
        main_widget = QWidget()
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # Tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Create tabs
        self.pages_tab = self.create_pages_tab()
        self.panels_tab = self.create_panels_tab()
        self.assets_tab = self.create_assets_tab()
        self.layers_tab = self.create_layers_tab()

        self.tabs.addTab(self.pages_tab, "Pages")
        self.tabs.addTab(self.panels_tab, "Panels")
        self.tabs.addTab(self.assets_tab, "Assets")
        self.tabs.addTab(self.layers_tab, "Layers")

        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

        self.setWidget(main_widget)

    def create_pages_tab(self):
        """Create pages management tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Page list
        self.page_list = QListWidget()
        self.page_list.setIconSize(QSize(64, 80))
        layout.addWidget(self.page_list)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("Add Page")
        btn_add.clicked.connect(self.add_page)
        btn_delete = QPushButton("Delete")
        btn_duplicate = QPushButton("Duplicate")

        btn_layout.addWidget(btn_add)
        btn_layout.addWidget(btn_duplicate)
        btn_layout.addWidget(btn_delete)
        layout.addLayout(btn_layout)

        widget.setLayout(layout)
        return widget

    def create_panels_tab(self):
        """Create panel templates tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Template selector
        template_label = QLabel("Panel Templates:")
        layout.addWidget(template_label)

        # Template grid
        scroll = QScrollArea()
        template_widget = QWidget()
        template_layout = QGridLayout()
        template_widget.setLayout(template_layout)

        # Add template buttons (would be populated dynamically)
        templates = [
            "2x3 Grid", "3x2 Grid", "Splash", "Hero Moment",
            "4-Panel Strip", "L-Shape", "Diagonal", "Custom"
        ]

        for i, template in enumerate(templates):
            btn = QPushButton(template)
            btn.setMinimumHeight(60)
            template_layout.addWidget(btn, i // 2, i % 2)

        scroll.setWidget(template_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)

        # Panel properties
        props_group = QGroupBox("Panel Properties")
        props_layout = QVBoxLayout()

        # Border width
        props_layout.addWidget(QLabel("Border Width:"))
        border_slider = QSlider(Qt.Horizontal)
        border_slider.setRange(0, 20)
        border_slider.setValue(4)
        props_layout.addWidget(border_slider)

        # Gutter size
        props_layout.addWidget(QLabel("Gutter Size:"))
        gutter_slider = QSlider(Qt.Horizontal)
        gutter_slider.setRange(0, 40)
        gutter_slider.setValue(12)
        props_layout.addWidget(gutter_slider)

        # Clip content
        clip_check = QCheckBox("Clip Content to Panel")
        clip_check.setChecked(True)
        props_layout.addWidget(clip_check)

        props_group.setLayout(props_layout)
        layout.addWidget(props_group)

        widget.setLayout(layout)
        return widget

    def create_assets_tab(self):
        """Create assets library tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Speech Bubbles section
        bubbles_group = QGroupBox("Speech Bubbles")
        bubbles_layout = QGridLayout()

        bubble_types = [
            "Standard", "Thought", "Shout",
            "Whisper", "Radio", "Narration"
        ]

        for i, bubble in enumerate(bubble_types):
            btn = QPushButton(bubble)
            btn.setMinimumHeight(50)
            bubbles_layout.addWidget(btn, i // 2, i % 2)

        bubbles_group.setLayout(bubbles_layout)
        layout.addWidget(bubbles_group)

        # SFX Library section
        sfx_group = QGroupBox("SFX Library")
        sfx_layout = QVBoxLayout()

        # Category selector
        sfx_category = QComboBox()
        sfx_category.addItems(["Impact", "Motion", "Sound", "Emotional"])
        sfx_layout.addWidget(sfx_category)

        # SFX buttons
        sfx_grid = QGridLayout()
        sfx_items = ["POW", "BAM", "CRASH", "ZOOM", "WHOOSH", "RING"]

        for i, sfx in enumerate(sfx_items):
            btn = QPushButton(sfx)
            btn.setMinimumHeight(40)
            sfx_grid.addWidget(btn, i // 2, i % 2)

        sfx_layout.addLayout(sfx_grid)
        sfx_group.setLayout(sfx_layout)
        layout.addWidget(sfx_group)

        # Image Import section
        import_group = QGroupBox("Image Import")
        import_layout = QVBoxLayout()

        btn_import = QPushButton("Import to Panel")
        btn_paste = QPushButton("Paste from Clipboard")

        import_layout.addWidget(btn_import)
        import_layout.addWidget(btn_paste)

        import_group.setLayout(import_layout)
        layout.addWidget(import_group)

        layout.addStretch()
        widget.setLayout(layout)
        return widget

    def create_layers_tab(self):
        """Create layers management tab"""
        widget = QWidget()
        layout = QVBoxLayout()

        # Layer list
        self.layer_list = QListWidget()
        layout.addWidget(self.layer_list)

        # Layer buttons
        btn_layout = QHBoxLayout()
        btn_new = QPushButton("New Layer")
        btn_delete = QPushButton("Delete")

        btn_layout.addWidget(btn_new)
        btn_layout.addWidget(btn_delete)
        layout.addLayout(btn_layout)

        widget.setLayout(layout)
        return widget

    def add_page(self):
        """Add new page to project"""
        from ..comic_manager import ComicProjectManager
        # Implementation would connect to project manager
        pass

    def refresh_project(self):
        """Refresh UI with current project data"""
        pass


class MultiPageComicsDockerFactory(DockWidgetFactory):
    """Factory for creating docker instances"""

    def __init__(self):
        super().__init__("multi_page_comics_docker", "Multi-Page Comics", MultiPageComicsDocker)

    def createDockWidget(self):
        return MultiPageComicsDocker()
