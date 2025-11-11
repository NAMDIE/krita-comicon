from PyQt5.QtCore import QPointF, QRectF
import math


def rect_from_percentages(page_width, page_height, x_pct, y_pct, w_pct, h_pct):
'''Convert percentage-based coordinates to pixel coordinates'''
return QRectF(
x_pct * page_width / 100,
y_pct * page_height / 100,
w_pct * page_width / 100,
h_pct * page_height / 100
)


def calculate_tail_point(bubble_center, target_point):
'''Calculate speech bubble tail attachment point'''
angle = math.atan2(
target_point.y() - bubble_center.y(),
target_point.x() - bubble_center.x()
)
return QPointF(
bubble_center.x() + math.cos(angle) * 50,
bubble_center.y() + math.sin(angle) * 30
)


def snap_to_grid(point, grid_size):
'''Snap point to grid'''
return QPointF(
round(point.x() / grid_size) * grid_size,
round(point.y() / grid_size) * grid_size
)


def rect_contains_rect(outer, inner):
'''Check if outer rectangle contains inner rectangle'''
return (outer.contains(inner.topLeft()) and
outer.contains(inner.bottomRight()))
