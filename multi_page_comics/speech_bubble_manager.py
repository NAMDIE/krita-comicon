from typing import Dict, Any, Optional
from PyQt5.QtGui import QPainterPath, QColor, QFont
from PyQt5.QtCore import QPointF, QRectF, Qt
import math


class SpeechBubbleManager:
    """Manages speech bubble creation and styling."""

    BUBBLE_STYLES = {
        'standard': 'rectangular',
        'thought': 'cloud',
        'shout': 'jagged',
        'whisper': 'rounded',
        'radio': 'circle',
        'narration': 'box'
    }

    def __init__(self):
        self.default_text_color = QColor(0, 0, 0)
        self.default_bg_color = QColor(255, 255, 255)
        self.default_border_color = QColor(0, 0, 0)
        self.default_border_width = 3

    def create_bubble(
        self,
        doc,
        layer,
        bubble_data: Dict[str, Any]
    ) -> Optional[Any]:
        """Create speech bubble shape.
        
        Args:
            doc: Krita document
            layer: Parent layer
            bubble_data: Bubble configuration dictionary
            
        Returns:
            Bubble vector layer or None if failed
        """
        style = bubble_data.get('style', 'standard')
        bounds = QRectF(
            bubble_data.get('x', 0),
            bubble_data.get('y', 0),
            bubble_data.get('width', 200),
            bubble_data.get('height', 100)
        )

        # Create bubble shape
        bubble_path = self._create_bubble_shape(style, bounds)

        # Create vector layer
        bubble_layer = doc.createVectorLayer(f"Bubble - {style}")
        layer.addChildNode(bubble_layer, None)

        # Create tail if specified
        if bubble_data.get('tail', False):
            tail_style = bubble_data.get('tail_style', 'curved')
            tail_point = QPointF(
                bubble_data.get('tail_x', bounds.center().x()),
                bubble_data.get('tail_y', bounds.bottom() + 30)
            )
            self._create_tail(bubble_layer, bounds, tail_point, tail_style)

        return bubble_layer

    def _create_bubble_shape(
        self,
        style: str,
        bounds: QRectF
    ) -> QPainterPath:
        """Generate bubble shape path.
        
        Args:
            style: Bubble style (standard, thought, shout, etc.)
            bounds: Bounding rectangle
            
        Returns:
            QPainterPath representing bubble shape
        """
        if style == 'cloud':
            return self._create_cloud_shape(bounds)
        elif style == 'jagged':
            return self._create_jagged_shape(bounds)
        elif style == 'rounded':
            return self._create_rounded_shape(bounds)
        else:
            # Standard rectangular bubble
            path = QPainterPath()
            path.addRect(bounds)
            return path

    def _create_cloud_shape(self, bounds: QRectF) -> QPainterPath:
        """Create cloud-shaped thought bubble.
        
        Args:
            bounds: Bounding rectangle
            
        Returns:
            QPainterPath for cloud shape
        """
        path = QPainterPath()
        radius = min(bounds.width(), bounds.height()) / 4
        center = bounds.center()

        # Create 8-bump cloud pattern
        bumps = 8
        for i in range(bumps):
            angle = (2 * math.pi * i) / bumps
            # Bump position on circle
            bump_x = center.x() + (bounds.width() / 2 - radius) * math.cos(angle)
            bump_y = center.y() + (bounds.height() / 2 - radius) * math.sin(angle)
            # Draw circular bump
            path.addEllipse(QPointF(bump_x, bump_y), radius, radius)

        return path

    def _create_jagged_shape(self, bounds: QRectF) -> QPainterPath:
        """Create jagged/shout bubble with spiky edges.
        
        Args:
            bounds: Bounding rectangle
            
        Returns:
            QPainterPath for jagged shape
        """
        path = QPainterPath()
        center = bounds.center()
        points = []

        # Create 16-point starburst pattern
        points_count = 16
        for i in range(points_count):
            angle = (2 * math.pi * i) / points_count
            # Alternate between inner and outer radius for jagged effect
            if i % 2 == 0:
                radius = max(bounds.width(), bounds.height()) / 2
            else:
                radius = max(bounds.width(), bounds.height()) / 3
            
            x = center.x() + radius * math.cos(angle)
            y = center.y() + radius * math.sin(angle)
            points.append(QPointF(x, y))

        # Create polygon from points
        if points:
            path.moveTo(points[0])
            for point in points[1:]:
                path.lineTo(point)
            path.closeSubpath()

        return path

    def _create_rounded_shape(self, bounds: QRectF) -> QPainterPath:
        """Create rounded rectangle shape.
        
        Args:
            bounds: Bounding rectangle
            
        Returns:
            QPainterPath for rounded rectangle
        """
        path = QPainterPath()
        radius = min(bounds.width(), bounds.height()) / 8
        path.addRoundedRect(bounds, radius, radius)
        return path

    def _create_tail(
        self,
        layer,
        bubble_bounds: QRectF,
        tail_point: QPointF,
        style: str = 'curved'
    ) -> None:
        """Create speech bubble tail.
        
        Args:
            layer: Vector layer to draw on
            bubble_bounds: Bubble bounding rectangle
            tail_point: Point where tail points
            style: Tail style (curved, sharp, bubble)
        """
        if style == 'curved':
            # Create curved tail using quadratic bezier
            path = QPainterPath()
            start = bubble_bounds.bottomRight()
            control = QPointF(
                (start.x() + tail_point.x()) / 2,
                (start.y() + tail_point.y()) / 2 - 20
            )
            path.moveTo(start)
            path.quadTo(control, tail_point)
            path.lineTo(bubble_bounds.bottomLeft())
            path.closeSubpath()

        elif style == 'sharp':
            # Create triangular pointed tail
            path = QPainterPath()
            path.moveTo(bubble_bounds.bottomRight())
            path.lineTo(tail_point)
            path.lineTo(bubble_bounds.bottomLeft())
            path.closeSubpath()

        elif style == 'bubble':
            # Create circular bubble tail
            tail_radius = 15
            path = QPainterPath()
            path.addEllipse(tail_point, tail_radius, tail_radius)

    def add_text_to_bubble(
        self,
        doc,
        bubble_layer,
        text: str,
        bubble_data: Dict[str, Any]
    ) -> Optional[Any]:
        """Add text layer to bubble.
        
        Args:
            doc: Krita document
            bubble_layer: Bubble vector layer
            text: Text content
            bubble_data: Bubble configuration
            
        Returns:
            Text layer or None if failed
        """
        # Create text layer
        text_layer = doc.createShapeLayer(f"Text - {text[:20]}")
        bubble_layer.addChildNode(text_layer, None)

        # Configure font
        font = QFont("Arial", bubble_data.get('font_size', 18))
        font.setBold(bubble_data.get('bold', False))
        font.setItalic(bubble_data.get('italic', False))

        # TODO: Position text in center of bubble bounds and apply proper rendering
        # Requires Krita text tool integration

        return text_layer