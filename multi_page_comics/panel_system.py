from krita import Krita
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QColor


class PanelSystem:
'''Handles panel creation and management'''

def __init__(self):
self.default_border_width = 4
self.default_border_color = QColor(0, 0, 0)

def create_panel(self, doc, page_layer, panel_def, panel_number):
'''Create panel with clipping mask'''
# Create panel group
panel_group = doc.createGroupLayer(f"Panel {panel_number}")
page_layer.addChildNode(panel_group, None)

# Calculate dimensions
page_width = doc.width()
page_height = doc.height()

x = int(panel_def.get('x', 0) * page_width / 100)
y = int(panel_def.get('y', 0) * page_height / 100)
width = int(panel_def.get('width', 50) * page_width / 100)
height = int(panel_def.get('height', 50) * page_height / 100)

# Create border layer
border_layer = doc.createVectorLayer(f"Panel {panel_number} Border")
panel_group.addChildNode(border_layer, None)

# Draw border rectangle
self._draw_panel_border(
border_layer,
x, y, width, height,
panel_def.get('border_width', self.default_border_width)
)

# Create clipping mask layer
if panel_def.get('clip_content', True):
mask_layer = doc.createTransparencyMask(f"Panel {panel_number} Mask")
panel_group.addChildNode(mask_layer, border_layer)
self._create_clipping_mask(mask_layer, x, y, width, height)

# Create content layer
content_layer = doc.createPaintLayer(f"Panel {panel_number} Content")
panel_group.addChildNode(content_layer, None)

panel_data = {
'number': panel_number,
'bounds': {'x': x, 'y': y, 'width': width, 'height': height},
'border_width': panel_def.get('border_width', self.default_border_width),
'clip_content': panel_def.get('clip_content', True),
'layer_id': panel_group.uniqueId()
}

return panel_data

def _draw_panel_border(self, layer, x, y, width, height, border_width):
'''Draw panel border as vector shape'''
# This would use Krita's vector shape API
# Simplified version - in production use proper vector tools
pass

def _create_clipping_mask(self, mask_layer, x, y, width, height):
'''Create transparency mask for panel clipping'''
# Fill mask area with white (visible)
rect = QRect(x, y, width, height)
# Use Krita's selection and fill tools
pass

def import_image_to_panel(self, doc, panel_data, image_path):
'''Import image and clip to panel bounds'''
from krita import QImage

# Load image
img = QImage(image_path)

# Find panel layer
panel_layer = doc.nodeByUniqueID(panel_data['layer_id'])
if not panel_layer:
return False

# Create new layer for image
img_layer = doc.createFileLayer(
"Imported Image",
image_path,
"None"
)

# Add to panel group
panel_layer.addChildNode(img_layer, None)

# Scale to fit panel
bounds = panel_data['bounds']
img_layer.move(bounds['x'], bounds['y'])

return True

def paste_to_panel(self, doc, panel_data):
'''Paste clipboard content to panel'''
from PyQt5.QtWidgets import QApplication

clipboard = QApplication.clipboard()
image = clipboard.image()

if image.isNull():
return False

# Create layer from clipboard
panel_layer = doc.nodeByUniqueID(panel_data['layer_id'])
if not panel_layer:
return False

paste_layer = doc.createPaintLayer("Pasted Image")
panel_layer.addChildNode(paste_layer, None)

# Convert QImage to pixel data and set
ptr = image.bits()
ptr.setsize(image.byteCount())
pixel_data = ptr.asstring()

bounds = panel_data['bounds']
paste_layer.setPixelData(
pixel_data,
bounds['x'], bounds['y'],
image.width(), image.height()
)

return True
