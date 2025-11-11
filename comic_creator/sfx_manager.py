from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt


class SFXManager:
'''Manages sound effect graphics library'''

def __init__(self):
self.sfx_library = self.load_sfx_library()

def load_sfx_library(self):
'''Load SFX presets'''
return {
'impact': {
'POW': {'color': '#FF0000', 'style': 'bold', 'outline': True},
'BAM': {'color': '#FF6600', 'style': 'bold', 'outline': True},
'CRASH': {'color': '#FFAA00', 'style': 'bold', 'outline': True},
'THUD': {'color': '#8B4513', 'style': 'bold', 'outline': True},
'SMASH': {'color': '#FF0000', 'style': 'bold', 'outline': True},
'WHAM': {'color': '#FF3300', 'style': 'bold', 'outline': True},
},
'motion': {
'ZOOM': {'color': '#0066FF', 'style': 'italic', 'outline': False},
'WHOOSH': {'color': '#00AAFF', 'style': 'italic', 'outline': False},
'SWING': {'color': '#00FF88', 'style': 'italic', 'outline': False},
'DASH': {'color': '#FF00FF', 'style': 'italic', 'outline': False},
'SWOOSH': {'color': '#00CCFF', 'style': 'italic', 'outline': False},
},
'sound': {
'RING': {'color': '#FFD700', 'style': 'bold', 'outline': True},
'BEEP': {'color': '#00FF00', 'style': 'bold', 'outline': True},
'BANG': {'color': '#FF0000', 'style': 'bold', 'outline': True},
'CLICK': {'color': '#808080', 'style': 'normal', 'outline': False},
'BUZZ': {'color': '#FFFF00', 'style': 'bold', 'outline': True},
},
'emotional': {
'GASP': {'color': '#ADD8E6', 'style': 'italic', 'outline': False},
'SOB': {'color': '#4169E1', 'style': 'italic', 'outline': False},
'SIGH': {'color': '#B0C4DE', 'style': 'italic', 'outline': False},
}
}

def add_sfx(self, doc, layer, sfx_text, category, position, size=48):
'''Add SFX text to layer'''
if category not in self.sfx_library:
category = 'impact'

sfx_data = self.sfx_library[category].get(
sfx_text,
{'color': '#FF0000', 'style': 'bold', 'outline': True}
)

# Create text layer
sfx_layer = doc.createVectorLayer(f"SFX - {sfx_text}")
layer.addChildNode(sfx_layer, None)

# Configure text properties
font = QFont("Arial", size)
if sfx_data['style'] == 'bold':
font.setBold(True)
elif sfx_data['style'] == 'italic':
font.setItalic(True)

# Position and style would be set via Krita's text API
return sfx_layer

def get_category_sfx(self, category):
'''Get all SFX in category'''
return self.sfx_library.get(category, {})

def add_custom_sfx(self, category, text, properties):
'''Add custom SFX to library'''
if category not in self.sfx_library:
self.sfx_library[category] = {}
self.sfx_library[category][text] = properties
