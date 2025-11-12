from typing import Tuple
from PyQt5.QtCore import QPointF, QRectF
import math


def rect_from_percentages(
    page_width: float,
    page_height: float,
    x_pct: float,
    y_pct: float,
    w_pct: float,
    h_pct: float
) -> QRectF:
    """Convert percentage-based coordinates to pixel coordinates.
    
    Args:
        page_width: Page width in pixels
        page_height: Page height in pixels
        x_pct: X percentage
        y_pct: Y percentage
        w_pct: Width percentage
        h_pct: Height percentage
        
    Returns:
        QRectF with pixel coordinates
    """
    return QRectF(
        x_pct * page_width / 100,
        y_pct * page_height / 100,
        w_pct * page_width / 100,
        h_pct * page_height / 100
    )


def calculate_tail_point(
    bubble_center: QPointF,
    target_point: QPointF,
    distance: float = 50
) -> QPointF:
    """Calculate speech bubble tail attachment point.
    
    Args:
        bubble_center: Center of speech bubble
        target_point: Target point for tail
        distance: Distance from bubble center
        
    Returns:
        QPointF for tail attachment
    """
    angle = math.atan2(
        target_point.y() - bubble_center.y(),
        target_point.x() - bubble_center.x()
    )
    return QPointF(
        bubble_center.x() + math.cos(angle) * distance,
        bubble_center.y() + math.sin(angle) * 30
    )


def snap_to_grid(point: QPointF, grid_size: float) -> QPointF:
    """Snap point to grid.
    
    Args:
        point: Point to snap
        grid_size: Grid cell size
        
    Returns:
        Snapped QPointF
    """
    return QPointF(
        round(point.x() / grid_size) * grid_size,
        round(point.y() / grid_size) * grid_size
    )


def rect_contains_rect(outer: QRectF, inner: QRectF) -> bool:
    """Check if outer rectangle contains inner rectangle.
    
    Args:
        outer: Outer rectangle
        inner: Inner rectangle
        
    Returns:
        True if outer contains inner
    """
    return (outer.contains(inner.topLeft()) and
            outer.contains(inner.bottomRight()))