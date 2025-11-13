from PyQt5.QtWidgets import (
	QDialog, QVBoxLayout, QHBoxLayout,
	QPushButton, QLabel, QComboBox, QSpinBox,
	QCheckBox, QLineEdit, QFileDialog, QGroupBox,
	QRadioButton, QButtonGroup, QProgressBar
)
from PyQt5.QtCore import Qt


class ExportDialog(QDialog):
	"""Dialog for exporting comic pages"""

	def __init__(self, project_manager, parent=None):
		super().__init__(parent)
		self.project_manager = project_manager
		self.setWindowTitle("Export Comic")
		self.resize(500, 600)

		self.init_ui()

	def init_ui(self):
		"""Initialize UI"""
		layout = QVBoxLayout()

		# Output location
		location_group = QGroupBox("Output Location")
		location_layout = QVBoxLayout()

		path_layout = QHBoxLayout()
		self.path_input = QLineEdit()
		btn_browse = QPushButton("Browse...")
		btn_browse.clicked.connect(self.browse_output)
		path_layout.addWidget(self.path_input)
		path_layout.addWidget(btn_browse)
		location_layout.addLayout(path_layout)

		location_group.setLayout(location_layout)
		layout.addWidget(location_group)

		# Format selection
		format_group = QGroupBox("Export Format")
		format_layout = QVBoxLayout()

		self.format_combo = QComboBox()
		self.format_combo.addItems(["PNG", "JPEG", "PDF", "CBZ", "PSD"])
		self.format_combo.currentTextChanged.connect(self.format_changed)
		format_layout.addWidget(self.format_combo)

		format_group.setLayout(format_layout)
		layout.addWidget(format_group)

		# Page range
		range_group = QGroupBox("Page Range")
		range_layout = QVBoxLayout()

		self.range_buttons = QButtonGroup()
		rb_all = QRadioButton("All Pages")
		rb_all.setChecked(True)
		rb_current = QRadioButton("Current Page Only")
		rb_range = QRadioButton("Page Range:")

		self.range_buttons.addButton(rb_all, 1)
		self.range_buttons.addButton(rb_current, 2)
		self.range_buttons.addButton(rb_range, 3)

		range_layout.addWidget(rb_all)
		range_layout.addWidget(rb_current)

		range_input_layout = QHBoxLayout()
		range_input_layout.addWidget(rb_range)
		self.range_start = QSpinBox()
		self.range_end = QSpinBox()
		range_input_layout.addWidget(QLabel("From:"))
		range_input_layout.addWidget(self.range_start)
		range_input_layout.addWidget(QLabel("To:"))
		range_input_layout.addWidget(self.range_end)
		range_layout.addLayout(range_input_layout)

		range_group.setLayout(range_layout)
		layout.addWidget(range_group)

		# Quality options
		quality_group = QGroupBox("Quality Options")
		quality_layout = QVBoxLayout()

		dpi_layout = QHBoxLayout()
		dpi_layout.addWidget(QLabel("DPI:"))
		self.dpi_spin = QSpinBox()
		self.dpi_spin.setRange(72, 600)
		self.dpi_spin.setValue(300)
		dpi_layout.addWidget(self.dpi_spin)
		dpi_layout.addStretch()
		quality_layout.addLayout(dpi_layout)

		self.flatten_check = QCheckBox("Flatten Layers")
		quality_layout.addWidget(self.flatten_check)

		self.bleed_check = QCheckBox("Include Bleed Marks")
		quality_layout.addWidget(self.bleed_check)

		quality_group.setLayout(quality_layout)
		layout.addWidget(quality_group)

		# Progress bar
		self.progress = QProgressBar()
		self.progress.setVisible(False)
		layout.addWidget(self.progress)

		# Buttons
		btn_layout = QHBoxLayout()
		btn_export = QPushButton("Export")
		btn_export.clicked.connect(self.start_export)
		btn_cancel = QPushButton("Cancel")
		btn_cancel.clicked.connect(self.reject)

		btn_layout.addStretch()
		btn_layout.addWidget(btn_export)
		btn_layout.addWidget(btn_cancel)
		layout.addLayout(btn_layout)

		self.setLayout(layout)

	def browse_output(self):
		"""Browse for output directory"""
		directory = QFileDialog.getExistingDirectory(
			self,
			"Select Output Directory"
		)
		if directory:
			self.path_input.setText(directory)

	def format_changed(self, format_text):
		"""Handle format change"""
		# Adjust options based on format
		if format_text == "JPEG":
			self.flatten_check.setChecked(True)
			self.flatten_check.setEnabled(False)
		else:
			self.flatten_check.setEnabled(True)

	def start_export(self):
		"""Start export process"""
		output_path = self.path_input.text()
		if not output_path:
			return

		format_text = self.format_combo.currentText().lower()

		options = {
			'dpi': self.dpi_spin.value(),
			'flatten': self.flatten_check.isChecked(),
			'bleed': self.bleed_check.isChecked()
		}

		self.progress.setVisible(True)

		from ..export_manager import ExportManager
		exporter = ExportManager()

		success = exporter.export_project(
			self.project_manager,
			output_path,
			format_text,
			options
		)

		if success:
			self.accept()
		else:
			self.progress.setVisible(False)
