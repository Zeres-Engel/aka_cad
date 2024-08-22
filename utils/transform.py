import numpy as np
from svgpathtools import parse_path

# Utility functions
def sort_points(points, clockwise=True):
    """Sort points in a numpy array clockwise or counterclockwise."""
    if points.size == 0:
        return points

    centroid = np.mean(points, axis=0)
    angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])
    sorted_indices = np.argsort(-angles if clockwise else angles)
    
    return points[sorted_indices]
# Utility functions
def rotate_points(points, angle, origin=(0, 0)):
    ox, oy = origin
    px, py = points.T  # Transpose to get x, y columns
    cos_angle, sin_angle = np.cos(angle), np.sin(angle)

    qx = ox + cos_angle * (px - ox) - sin_angle * (py - oy)
    qy = oy + sin_angle * (px - ox) + cos_angle * (py - oy)

    return np.column_stack([qx, qy])


def calculate_centroid(points):
    """Calculate the centroid of a set of points."""
    return np.mean(points, axis=0)

def transform_svg_element(elem, polygon, dx=0, dy=0, angle=0):
    """Apply transformation to an SVG element based on polygon and translation."""
    polygon_centroid = calculate_centroid(polygon) + np.array([dx, dy])
    # Chuyển đổi chức năng dựa trên nhãn SVG tag
    tag = elem.tag.split('}')[-1]

    transform_functions = {
        'rect': apply_transform_to_rect,
        'circle': apply_transform_to_circle_or_ellipse,
        'ellipse': apply_transform_to_circle_or_ellipse,
        'line': apply_transform_to_line,
        'polyline': apply_transform_to_polyline_or_polygon,
        'polygon': apply_transform_to_polyline_or_polygon,
        'path': apply_transform_to_path,
        'g': apply_transform_to_group,
        'image': apply_transform_to_image
    }

    if tag in transform_functions:
        transform_functions[tag](elem, polygon_centroid, angle)

    return elem

def apply_transform_to_rect(elem, centroid, angle):
    """Apply transformation to a rectangle element."""
    width, height = int(elem.get('width', 0)), int(elem.get('height', 0))
    x, y = float(centroid[0]) - width / 2, float(centroid[1]) - height / 2
    points = np.array([[x, y], [x + width, y], [x + width, y + height], [x, y + height]])
    rotated_points = np.array([rotate_point(point, angle, origin=centroid) for point in points])

    min_x, min_y = np.min(rotated_points, axis=0)
    max_x, max_y = np.max(rotated_points, axis=0)
    elem.set('x', str(min_x))
    elem.set('y', str(min_y))
    elem.set('width', str(width))
    elem.set('height', str(height))

def apply_transform_to_circle_or_ellipse(elem, centroid, angle):
    """Apply transformation to a circle or ellipse element."""
    cx, cy = rotate_point((centroid[0], centroid[1]), angle, origin=centroid)
    elem.set('cx', str(cx))
    elem.set('cy', str(cy))

def apply_transform_to_line(elem, centroid, angle):
    """Apply transformation to a line element."""
    x1, y1 = float(elem.get('x1', 0)), float(elem.get('y1', 0))
    x2, y2 = float(elem.get('x2', 0)), float(elem.get('y2', 0))
    midpoint = np.array([(x1 + x2) / 2, (y1 + y2) / 2])
    delta = centroid - midpoint

    x1, y1 = rotate_point((x1 + delta[0], y1 + delta[1]), angle, origin=centroid)
    x2, y2 = rotate_point((x2 + delta[0], y2 + delta[1]), angle, origin=centroid)

    elem.set('x1', str(x1))
    elem.set('y1', str(y1))
    elem.set('x2', str(x2))
    elem.set('y2', str(y2))

def apply_transform_to_polyline_or_polygon(elem, centroid, angle):
    """Apply transformation to a polyline or polygon element."""
    points = np.array([[float(coord) for coord in point.split(',')] for point in elem.get('points', '').strip().split()])
    current_centroid = calculate_centroid(points)
    delta = centroid - current_centroid
    moved_points = points + delta
    rotated_points = np.array([rotate_point(point, angle, origin=centroid) for point in moved_points])
    points_str = ' '.join([f"{x},{y}" for x, y in rotated_points])
    elem.set('points', points_str)

def apply_transform_to_path(elem, centroid, angle):
    """Apply transformation to a path element."""
    path = parse_path(elem.get('d', ''))
    points = np.array([[seg.start.real, seg.start.imag] for seg in path] +
                      [[seg.end.real, seg.end.imag] for seg in path])
    current_centroid = calculate_centroid(points)
    delta = centroid - current_centroid

    path_d = ""
    for seg in path:
        start = rotate_point(np.array([seg.start.real, seg.start.imag]) + delta, angle, origin=centroid)
        end = rotate_point(np.array([seg.end.real, seg.end.imag]) + delta, angle, origin=centroid)
        cmd = f"M{start[0]},{start[1]} L{end[0]},{end[1]} "
        path_d += cmd
    elem.set('d', path_d.strip())

def apply_transform_to_group(elem, centroid, angle):
    """Apply transformation to a group element."""
    for child in elem:
        transform_svg_element(child, [centroid], angle=angle)

def apply_transform_to_image(elem, centroid, angle):
    """Apply transformation to an image element."""
    width, height = float(elem.get('width', 0)), float(elem.get('height', 0))
    x, y = centroid[0] - width / 2, centroid[1] - height / 2
    points = np.array([[x, y], [x + width, y], [x + width, y + height], [x, y + height]])
    rotated_points = np.array([rotate_point(point, angle, origin=centroid) for point in points])

    min_x, min_y = np.min(rotated_points, axis=0)
    max_x, max_y = np.max(rotated_points, axis=0)
    elem.set('x', str(min_x))
    elem.set('y', str(min_y))
    elem.set('width', str(int(width)))
    elem.set('height', str(int(height)))

# Rotation function
def transform_rotation(elem, bin_elem):
    """Apply the rotation from bin_elem to elem."""
    bin_transform = bin_elem.get('transform', '')
    elem.set('transform', bin_transform)
    return elem