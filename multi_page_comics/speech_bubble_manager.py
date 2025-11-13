from typing import Dict, Any, Optional
from PyQt5.QtCore import QPointF, QRectF
from PyQt5.QtGui import QPainterPath, QColor, QFont
import math


class SpeechBubbleManager:
    """Manages speech bubble creation and simple rendering helpers."""

    def __init__(self):
        self.default_text_color = QColor(0, 0, 0)
        self.default_bg_color = QColor(255, 255, 255)
        self.default_border_color = QColor(0, 0, 0)
        self.default_border_width = 3

        self.bubble_presets = {
            'standard': {'name': 'Standard', 'style': 'rounded'},
            'thought': {'name': 'Thought', 'style': 'cloud'},
            'shout': {'name': 'Shout', 'style': 'jagged'},
            'whisper': {'name': 'Whisper', 'style': 'rounded'},
            'radio': {'name': 'Radio', 'style': 'rounded'},
            'narration': {'name': 'Narration', 'style': 'rectangle'}
        }

    def create_bubble(self, doc, layer, bubble_data: Dict[str, Any]):
        """Create a speech bubble vector layer and return it.

        This is a minimal implementation: it creates a vector layer and
        computes a QPainterPath for the requested style. Integrating the
        path into Krita's vector objects requires Krita API calls and is
        left as TODO comments where appropriate.
        """
        style = bubble_data.get('style', 'standard')
        preset = self.bubble_presets.get(style, self.bubble_presets['standard'])

        bounds = QRectF(
            bubble_data.get('x', 0),
            bubble_data.get('y', 0),
            bubble_data.get('width', 200),
            bubble_data.get('height', 100)
        )

        path = self._create_bubble_shape(preset['style'], bounds)

        # Create vector layer (placeholder - real usage should add path to vector layer)
        bubble_layer = doc.createVectorLayer(f"Bubble - {preset['name']}")
        layer.addChildNode(bubble_layer, None)

        # TODO: convert QPainterPath into Krita vector shape on bubble_layer

        # Optionally create tail
        if bubble_data.get('tail'):
            tail_point = QPointF(bubble_data.get('tail_x', bounds.center().x()),
                                 bubble_data.get('tail_y', bounds.bottom() + 30))
            tail_path = self._create_tail(bounds, tail_point, bubble_data.get('tail_style', 'curved'))
            # TODO: add tail_path to bubble_layer vector content

        return bubble_layer

    def _create_bubble_shape(self, style: str, bounds: QRectF) -> QPainterPath:
        """Return a QPainterPath for the requested bubble style."""
        if style == 'cloud':
            return self._create_cloud_shape(bounds)
        if style == 'jagged':
            return self._create_jagged_shape(bounds)
        if style == 'rectangle':
            p = QPainterPath()
            p.addRect(bounds)
            return p
        # default: rounded rectangle
        return self._create_rounded_shape(bounds)

    def _create_cloud_shape(self, bounds: QRectF) -> QPainterPath:
        path = QPainterPath()
        center = bounds.center()
        radius = min(bounds.width(), bounds.height()) / 4
        bumps = 8
        # place circular bumps around the bounds center
        for i in range(bumps):
            angle = (2 * math.pi * i) / bumps
            bump_x = center.x() + (bounds.width() / 2 - radius) * math.cos(angle)
            bump_y = center.y() + (bounds.height() / 2 - radius) * math.sin(angle)
            path.addEllipse(QPointF(bump_x, bump_y), radius, radius)
        return path

    def _create_jagged_shape(self, bounds: QRectF) -> QPainterPath:
        path = QPainterPath()
        center = bounds.center()
        points_count = 16
        points = []
        for i in range(points_count):
            angle = (2 * math.pi * i) / points_count
            radius = (bounds.width() + bounds.height()) / 4
            if i % 2 == 0:
                r = radius
            else:
                r = radius * 0.6
            x = center.x() + r * math.cos(angle)
            y = center.y() + r * math.sin(angle)
            points.append(QPointF(x, y))
        if points:
            path.moveTo(points[0])
            for p in points[1:]:
                path.lineTo(p)
            path.closeSubpath()
        return path

    def _create_rounded_shape(self, bounds: QRectF) -> QPainterPath:
        path = QPainterPath()
        radius = min(bounds.width(), bounds.height()) / 8
        path.addRoundedRect(bounds, radius, radius)
        return path

    def _create_tail(self, bubble_bounds: QRectF, tail_point: QPointF, style: str = 'curved') -> QPainterPath:
        """Create a simple tail path attached to bubble_bounds pointing to tail_point."""
        path = QPainterPath()
        start = bubble_bounds.center()
        if style == 'curved':
            control = QPointF((start.x() + tail_point.x()) / 2, (start.y() + tail_point.y()) / 2)
            path.moveTo(start)
            path.quadTo(control, tail_point)
        elif style == 'sharp':
            path.moveTo(bubble_bounds.bottomRight())
            path.lineTo(tail_point)
            path.lineTo(bubble_bounds.bottomLeft())
            path.closeSubpath()
        else:
            # bubble style
            path.addEllipse(tail_point, 8, 8)
        return path

    def add_text_to_bubble(self, doc, bubble_layer, text: str, bubble_data: Dict[str, Any]):
        """Create a placeholder text layer for the bubble and return it."""
        # Minimal placeholder implementation
        text_layer = doc.createVectorLayer(f"Bubble Text - {text[:20]}")
        bubble_layer.addChildNode(text_layer, None)
        # TODO: integrate with Krita text API to set text and layout
        return text_layer
