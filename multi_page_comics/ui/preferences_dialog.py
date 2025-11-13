from PyQt5.QtWidgets import (
	QDialog, QVBoxLayout, QHBoxLayout,
	QPushButton, QLabel, QLineEdit, QComboBox,
	QSpinBox, QGroupBox, QFormLayout
)
from PyQt5.QtCore import Qt


class NewProjectDialog(QDialog):
	"""Dialog for creating new comic project"""

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle("New Comic Project")
		self.resize(500, 450)

		self.init_ui()

	def init_ui(self):
		"""Initialize UI"""
		layout = QVBoxLayout()

		# Metadata group
		metadata_group = QGroupBox("Project Information")
		metadata_layout = QFormLayout()

		self.title_input = QLineEdit()
		self.author_input = QLineEdit()
		self.series_input = QLineEdit()
		self.issue_spin = QSpinBox()
		self.issue_spin.setMinimum(1)
		self.issue_spin.setValue(1)

		metadata_layout.addRow("Title:", self.title_input)
		metadata_layout.addRow("Author:", self.author_input)
		metadata_layout.addRow("Series:", self.series_input)
		metadata_layout.addRow("Issue #:", self.issue_spin)

		metadata_group.setLayout(metadata_layout)
		layout.addWidget(metadata_group)

		# Page format group
		format_group = QGroupBox("Page Format")
		format_layout = QFormLayout()

		self.format_combo = QComboBox()
		self.format_combo.addItems([
			'US Standard (6.625" × 10.25")',
			'Manga B6 (128mm × 182mm)',
			'European A4',
			'Webcomic (800px wide)',
			'Custom'
		])
		self.format_combo.currentTextChanged.connect(self.format_changed)

		self.width_spin = QSpinBox()
		self.width_spin.setRange(100, 10000)
		self.width_spin.setValue(1988)

		self.height_spin = QSpinBox()
		self.height_spin.setRange(100, 15000)
		self.height_spin.setValue(3056)

		self.dpi_spin = QSpinBox()
		self.dpi_spin.setRange(72, 600)
		self.dpi_spin.setValue(300)

		format_layout.addRow("Preset:", self.format_combo)
		format_layout.addRow("Width (px):", self.width_spin)
		format_layout.addRow("Height (px):", self.height_spin)
		format_layout.addRow("DPI:", self.dpi_spin)

		format_group.setLayout(format_layout)
		layout.addWidget(format_group)

		# Default settings group
		settings_group = QGroupBox("Default Settings")
		settings_layout = QFormLayout()

		self.gutter_spin = QSpinBox()
		self.gutter_spin.setRange(0, 50)
		self.gutter_spin.setValue(12)

		self.margin_spin = QSpinBox()
		self.margin_spin.setRange(0, 100)
		self.margin_spin.setValue(16)

		settings_layout.addRow("Gutter Size (px):", self.gutter_spin)
		settings_layout.addRow("Page Margin (px):", self.margin_spin)

		settings_group.setLayout(settings_layout)
		layout.addWidget(settings_group)

		# Buttons
		btn_layout = QHBoxLayout()
		btn_create = QPushButton("Create Project")
		btn_create.clicked.connect(self.accept)
		btn_cancel = QPushButton("Cancel")
		btn_cancel.clicked.connect(self.reject)

		btn_layout.addStretch()
		btn_layout.addWidget(btn_create)
		btn_layout.addWidget(btn_cancel)
		layout.addLayout(btn_layout)

		self.setLayout(layout)

	def format_changed(self, format_text):
		"""Update dimensions based on preset"""
		presets = {
			"US Standard": (1988, 3056, 300),
			"Manga B6": (1122, 1594, 300),
			"European A4": (2480, 3508, 300),
			"Webcomic": (800, 6000, 72)
		}

		for preset_name, (w, h, dpi) in presets.items():
			if preset_name in format_text:
				self.width_spin.setValue(w)
				self.height_spin.setValue(h)
				self.dpi_spin.setValue(dpi)
				break

	def get_project_data(self):
		"""Get project configuration data"""
		return {
			'title': self.title_input.text(),
			'author': self.author_input.text(),
			'series': self.series_input.text(),
			'issue': self.issue_spin.value(),
			'page_width': self.width_spin.value(),
			'page_height': self.height_spin.value(),
			'dpi': self.dpi_spin.value(),
			'gutter': self.gutter_spin.value(),
			'margin': self.margin_spin.value()
		}
