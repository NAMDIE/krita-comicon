from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
QPushButton, QLabel, QLineEdit, QComboBox,
QSpinBox, QSlider, QCheckBox, QWidget,
QGraphicsView, QGraphicsScene, QGraphicsRectItem)
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QBrush, QColor


class TemplateEditorDialog(QDialog):
'''Dialog for creating/editing panel templates'''

def __init__(self, template=None, parent=None):
super().__init__(parent)
self.template = template or self.create_default_template()
self.setWindowTitle("Panel Template Editor")
self.resize(1000, 700)

self.init_ui()

def init_ui(self):
'''Initialize UI'''
layout = QHBoxLayout()

# Left sidebar - properties
sidebar = self.create_sidebar()
layout.addWidget(sidebar)

# Center - canvas
self.canvas = self.create_canvas()
layout.addWidget(self.canvas, stretch=1)

# Right sidebar - panel list
panel_list = self.create_panel_list()
layout.addWidget(panel_list)

self.setLayout(layout)

def create_sidebar(self):
'''Create properties sidebar'''
widget = QWidget()
layout = QVBoxLayout()

# Template name
layout.addWidget(QLabel("Template Name:"))
self.name_input = QLineEdit(self.template.get('name', ''))
layout.addWidget(self.name_input)

# Category
layout.addWidget(QLabel("Category:"))
self.category_combo = QComboBox()
self.category_combo.addItems([
"Standard", "Western", "Manga", "European",
"Action", "Dialogue", "Splash", "Custom"
])
layout.addWidget(self.category_combo)

# Gutter size
layout.addWidget(QLabel("Gutter Size:"))
self.gutter_spin = QSpinBox()
self.gutter_spin.setRange(0, 50)
self.gutter_spin.setValue(12)
layout.addWidget(self.gutter_spin)

# Margin
layout.addWidget(QLabel("Page Margin:"))
self.margin_spin = QSpinBox()
self.margin_spin.setRange(0, 100)
self.margin_spin.setValue(16)
layout.addWidget(self.margin_spin)

# Tools
layout.addWidget(QLabel("Tools:"))
btn_add_rect = QPushButton("Add Rectangle Panel")
btn_add_rect.clicked.connect(self.add_rectangle_panel)
layout.addWidget(btn_add_rect)

btn_split_h = QPushButton("Split Horizontal")
layout.addWidget(btn_split_h)

btn_split_v = QPushButton("Split Vertical")
layout.addWidget(btn_split_v)

layout.addStretch()

# Action buttons
btn_save = QPushButton("Save Template")
btn_save.clicked.connect(self.save_template)
layout.addWidget(btn_save)

btn_cancel = QPushButton("Cancel")
btn_cancel.clicked.connect(self.reject)
layout.addWidget(btn_cancel)

widget.setLayout(layout)
widget.setMaximumWidth(250)
return widget

def create_canvas(self):
'''Create editing canvas'''
view = QGraphicsView()
self.scene = QGraphicsScene()
view.setScene(self.scene)

# Draw page boundary
page_rect = QRectF(0, 0, 600, 800)
self.scene.addRect(page_rect, QPen(QColor(200, 200, 200)))

# Draw existing panels
for panel in self.template.get('panels', []):
self.draw_panel(panel)

return view

def create_panel_list(self):
'''Create panel list sidebar'''
widget = QWidget()
layout = QVBoxLayout()

layout.addWidget(QLabel("Panels:"))

# Panel list would go here

widget.setLayout(layout)
widget.setMaximumWidth(200)
return widget

def draw_panel(self, panel_def):
'''Draw panel on canvas'''
x = panel_def.get('x', 0) * 6
y = panel_def.get('y', 0) * 8
w = panel_def.get('width', 50) * 6
h = panel_def.get('height', 50) * 8

rect_item = QGraphicsRectItem(x, y, w, h)
rect_item.setPen(QPen(QColor(0, 0, 0), 2))
rect_item.setBrush(QBrush(QColor(200, 220, 255, 100)))
self.scene.addItem(rect_item)

def add_rectangle_panel(self):
'''Add new rectangle panel'''
# Add default panel at center
new_panel = {
'x': 25,
'y': 25,
'width': 50,
'height': 50
}
self.template.setdefault('panels', []).append(new_panel)
self.draw_panel(new_panel)

def save_template(self):
'''Save template data'''
self.template['name'] = self.name_input.text()
self.template['category'] = self.category_combo.currentText().lower()
self.accept()

def get_template(self):
'''Get edited template data'''
return self.template

def create_default_template(self):
'''Create default empty template'''
return {
'id': 'custom',
'name': 'New Template',
'category': 'custom',
'panels': []
}
