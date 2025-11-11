from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPainterPath, QColor


class SpeechBubbleManager:
'''Manages speech bubble creation and library'''

def __init__(self):
self.bubble_presets = self.load_presets()

def load_presets(self):
'''Load speech bubble presets'''
return {
'standard': {
'name': 'Standard Speech',
'shape': 'ellipse',
'border_width': 2,
'tail_style': 'curved'
},
'thought': {
'name': 'Thought Bubble',
'shape': 'cloud',
'border_width': 2,
'tail_style': 'bubbles'
},
'shout': {
'name': 'Shout',
'shape': 'jagged',
'border_width': 3,
'tail_style': 'sharp'
},
'whisper': {
'name': 'Whisper',
'shape': 'ellipse',
'border_width': 1,
'border_style': 'dashed',
'tail_style': 'thin'
},
'radio': {
'name': 'Radio/Electronic',
'shape': 'rectangle',
'border_width': 2,
'border_style': 'zigzag',
'tail_style': 'lightning'
},
'narration': {
'name': 'Narration Box',
'shape': 'rectangle',
'border_width': 2,
'tail_style': None
}
}

def create_bubble(self, doc, layer, bubble_type, position, size, tail_point=None):
'''Create speech bubble on specified layer'''
preset = self.bubble_presets.get(bubble_type, self.bubble_presets['standard'])

# Create vector layer for bubble
bubble_layer = doc.createVectorLayer(f"Speech Bubble - {preset['name']}")
layer.addChildNode(bubble_layer, None)

# Create bubble shape based on preset
path = self._create_bubble_shape(
preset['shape'],
position,
size
)

# Add tail if specified
if tail_point and preset.get('tail_style'):
tail_path = self._create_tail(
preset['tail_style'],
position,
tail_point
)
path.addPath(tail_path)

# Apply to vector layer (simplified - actual implementation uses Krita vector API)
return bubble_layer

def _create_bubble_shape(self, shape_type, position, size):
'''Create bubble shape path'''
path = QPainterPath()
rect = QRectF(position.x(), position.y(), size.width(), size.height())

if shape_type == 'ellipse':
path.addEllipse(rect)
elif shape_type == 'rectangle':
path.addRect(rect)
elif shape_type == 'cloud':
# Create cloud-like shape with multiple circles
self._create_cloud_shape(path, rect)
elif shape_type == 'jagged':
# Create jagged edges for shout
self._create_jagged_shape(path, rect)

return path

def _create_cloud_shape(self, path, rect):
'''Create cloud bubble shape'''
# Simplified cloud - multiple overlapping circles
num_bumps = 8
for i in range(num_bumps):
angle = (i / num_bumps) * 360
# Add circle bumps around perimeter
pass

def _create_jagged_shape(self, path, rect):
'''Create jagged/burst shape for shouts'''
# Create star-burst pattern
pass

def _create_tail(self, tail_style, bubble_pos, target_pos):
'''Create speech bubble tail'''
path = QPainterPath()

if tail_style == 'curved':
# Smooth curved tail
path.moveTo(bubble_pos)
control = QPointF(
(bubble_pos.x() + target_pos.x()) / 2,
bubble_pos.y()
)
path.quadTo(control, target_pos)

elif tail_style == 'sharp':
# Angular tail for shouts
path.moveTo(bubble_pos)
path.lineTo(target_pos)

elif tail_style == 'bubbles':
# Small circles for thought bubble
for i in range(3):
t = (i + 1) / 4
x = bubble_pos.x() + t * (target_pos.x() - bubble_pos.x())
y = bubble_pos.y() + t * (target_pos.y() - bubble_pos.y())
radius = 10 - (i * 3)
path.addEllipse(QPointF(x, y), radius, radius)

return path

def add_text_to_bubble(self, doc, bubble_layer, text, font_size=12):
'''Add text to speech bubble'''
# Create text layer
text_layer = doc.createVectorLayer(f"Bubble Text")
bubble_layer.parentNode().addChildNode(text_layer, bubble_layer)

# Position text in center of bubble
# Use Krita's text tool API
return text_layer
