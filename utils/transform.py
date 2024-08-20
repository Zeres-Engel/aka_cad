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

def rotate_point(point, angle, origin=(0, 0)):
    """Rotate a point around a given origin."""
    ox, oy = origin
    px, py = point
    cos_angle, sin_angle = np.cos(angle), np.sin(angle)

    qx = ox + cos_angle * (px - ox) - sin_angle * (py - oy)
    qy = oy + sin_angle * (px - ox) + cos_angle * (py - oy)
    
    return qx, qy

def calculate_centroid(points):
    """Calculate the centroid of a set of points."""
    return np.mean(points, axis=0)

# Transform functions
def transform_svg_element(elem, polygon, dx=0, dy=0, angle=0):
    """Apply transformation to an SVG element based on polygon, dx, dy, and angle."""
    rotated_polygon = np.array([rotate_point(point, np.radians(angle)) for point in polygon])
    new_centroid = calculate_centroid(rotated_polygon)
    delta_x, delta_y = new_centroid - calculate_centroid(polygon)

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
        transform_functions[tag](elem, dx + delta_x, dy + delta_y, angle, new_centroid)

    return elem

def apply_transform_to_rect(elem, dx, dy, angle, centroid):
    """Apply transformation to a rectangle element."""
    x, y = float(elem.get('x', 0)) + dx, float(elem.get('y', 0)) + dy
    width, height = float(elem.get('width', 0)), float(elem.get('height', 0))
    points = np.array([[x, y], [x + width, y], [x + width, y + height], [x, y + height]])
    rotated_points = np.array([rotate_point(point, np.radians(angle), origin=centroid) for point in points])

    min_x, min_y = np.min(rotated_points, axis=0)
    max_x, max_y = np.max(rotated_points, axis=0)
    elem.set('x', str(min_x))
    elem.set('y', str(min_y))
    elem.set('width', str(max_x - min_x))
    elem.set('height', str(max_y - min_y))

def apply_transform_to_circle_or_ellipse(elem, dx, dy, angle, centroid):
    """Apply transformation to a circle or ellipse element."""
    cx, cy = float(elem.get('cx', 0)) + dx, float(elem.get('cy', 0)) + dy
    rotated_cx, rotated_cy = rotate_point((cx, cy), np.radians(angle), origin=centroid)
    elem.set('cx', str(rotated_cx))
    elem.set('cy', str(rotated_cy))

def apply_transform_to_line(elem, dx, dy, angle, centroid):
    """Apply transformation to a line element."""
    x1, y1 = float(elem.get('x1', 0)) + dx, float(elem.get('y1', 0)) + dy
    x2, y2 = float(elem.get('x2', 0)) + dx, float(elem.get('y2', 0)) + dy
    rotated_x1, rotated_y1 = rotate_point((x1, y1), np.radians(angle), origin=centroid)
    rotated_x2, rotated_y2 = rotate_point((x2, y2), np.radians(angle), origin=centroid)
    elem.set('x1', str(rotated_x1))
    elem.set('y1', str(rotated_y1))
    elem.set('x2', str(rotated_x2))
    elem.set('y2', str(rotated_y2))

def apply_transform_to_polyline_or_polygon(elem, dx, dy, angle, centroid):
    """Apply transformation to a polyline or polygon element."""
    points = np.array([[float(coord) for coord in point.split(',')] for point in elem.get('points', '').strip().split()])
    translated_points = points + np.array([dx, dy])
    rotated_points = np.array([rotate_point(point, np.radians(angle), origin=centroid) for point in translated_points])
    points_str = ' '.join([f"{x},{y}" for x, y in rotated_points])
    elem.set('points', points_str)

def apply_transform_to_path(elem, dx, dy, angle, centroid):
    """Apply transformation to a path element."""
    path = parse_path(elem.get('d', ''))
    points = np.array([[seg.start.real, seg.start.imag] for seg in path] +
                      [[seg.end.real, seg.end.imag] for seg in path])
    translated_points = points + np.array([dx, dy])
    rotated_points = np.array([rotate_point(point, np.radians(angle), origin=centroid) for point in translated_points])

    path_d = ""
    for i, point in enumerate(rotated_points):
        cmd = "M" if i == 0 else "L"
        path_d += f"{cmd}{point[0]},{point[1]} "
    path_d = path_d.strip() + "Z" if 'polygon' in elem.tag else path_d.strip()
    elem.set('d', path_d)

def apply_transform_to_group(elem, dx, dy, angle):
    """Apply transformation to a group element."""
    all_points = []
    for child in elem:
        if child.tag.split('}')[-1] in {'rect', 'circle', 'ellipse', 'line', 'polyline', 'polygon', 'path'}:
            child_points = np.array([[float(child.get('x', 0)), float(child.get('y', 0))]
                                     if 'x' in child.attrib and 'y' in child.attrib else [0, 0]])
            all_points.extend(child_points)

    group_centroid = calculate_centroid(np.array(all_points)) if all_points else (0, 0)
    for child in elem:
        transform_svg_element(child, all_points, dx, dy, angle)

    for child in elem:
        points = np.array([[float(coord) for coord in point.split(',')] for point in child.get('points', '').strip().split()])
        rotated_points = np.array([rotate_point(point, np.radians(angle), origin=group_centroid) for point in points])
        points_str = ' '.join([f"{x},{y}" for x, y in rotated_points])
        child.set('points', points_str)

def apply_transform_to_image(elem, dx, dy, angle, centroid):
    """Apply transformation to an image element."""
    x, y = float(elem.get('x', 0)) + dx, float(elem.get('y', 0)) + dy
    width, height = float(elem.get('width', 0)), float(elem.get('height', 0))
    points = np.array([[x, y], [x + width, y], [x + width, y + height], [x, y + height]])
    rotated_points = np.array([rotate_point(point, np.radians(angle), origin=centroid) for point in points])

    min_x, min_y = np.min(rotated_points, axis=0)
    max_x, max_y = np.max(rotated_points, axis=0)
    elem.set('x', str(min_x))
    elem.set('y', str(min_y))
    elem.set('width', str(max_x - min_x))
    elem.set('height', str(max_y - min_y))

# Rotation function
def transform_rotation(elem, bin_elem):
    """Apply the rotation from bin_elem to elem."""
    bin_transform = bin_elem.get('transform', '')
    elem.set('transform', bin_transform)
    return elem
