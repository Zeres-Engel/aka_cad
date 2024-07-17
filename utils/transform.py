import numpy as np
from svgpathtools import svg2paths, wsvg, Path, Line, CubicBezier, QuadraticBezier, Arc

def sort_points(points, clockwise=True):
    """ Sort points in a numpy array clockwise or counterclockwise, ensuring the array is two-dimensional. """
    if points.size == 0:
        return points  # Return empty array directly if no points are present.

    # Ensure points array is two-dimensional and has exactly two columns
    if points.ndim == 1:
        points = np.expand_dims(points, axis=0)
    if points.shape[1] != 2:
        raise ValueError("Points array must have exactly two columns (x and y coordinates).")

    centroid = np.mean(points, axis=0)
    angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])
    if not clockwise:
        angles = -angles
    sorted_points = points[np.argsort(-angles)]

    # Ensure the start point is also the end point for closed polygons
    if not np.array_equal(sorted_points[0], sorted_points[-1]):
        sorted_points = np.vstack([sorted_points, sorted_points[0]])
    return sorted_points

def align_edges(polygon, threshold_angle=3):
    """ Align edges to make them more horizontal or vertical based on a threshold angle. """
    if polygon is None:
        return None
    new_polygon = np.copy(polygon)
    num_points = len(polygon) - 1

    for i in range(num_points):
        p1, p2 = polygon[i], polygon[i + 1]
        dx, dy = p2 - p1
        angle = np.degrees(np.arctan2(dy, dx))
        angle = abs(angle) % 180
        if angle <= threshold_angle or angle >= (180 - threshold_angle):
            new_polygon[i + 1, 1] = new_polygon[i, 1]
        elif (angle >= (90 - threshold_angle)) and (angle <= (90 + threshold_angle)):
            new_polygon[i + 1, 0] = new_polygon[i, 0]
    return new_polygon

def rotate_point(point, angle, origin=(0, 0)):
    """ Rotate a point around a given origin. """
    angle_rad = angle
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle_rad) * (px - ox) - np.sin(angle_rad) * (py - oy)
    qy = oy + np.sin(angle_rad) * (px - ox) + np.cos(angle_rad) * (py - oy)
    return qx, qy

def translate_path(path, dx, dy):
    """ Translate a path by dx and dy. """
    new_segments = []
    for segment in path:
        if isinstance(segment, Line):
            start = segment.start + complex(dx, dy)
            end = segment.end + complex(dx, dy)
            new_segments.append(Line(start, end))
        elif isinstance(segment, CubicBezier):
            start = segment.start + complex(dx, dy)
            control1 = segment.control1 + complex(dx, dy)
            control2 = segment.control2 + complex(dx, dy)
            end = segment.end + complex(dx, dy)
            new_segments.append(CubicBezier(start, control1, control2, end))
        elif isinstance(segment, QuadraticBezier):
            start = segment.start + complex(dx, dy)
            control = segment.control + complex(dx, dy)
            end = segment.end + complex(dx, dy)
            new_segments.append(QuadraticBezier(start, control, end))
        elif isinstance(segment, Arc):
            start = segment.start + complex(dx, dy)
            end = segment.end + complex(dx, dy)
            new_segments.append(Arc(start, segment.radius, segment.rotation, segment.arc, segment.sweep, end))
        else:
            raise TypeError("Unsupported segment type")
    return Path(*new_segments)

def rotate_path(path, angle_degrees, origin=(0, 0)):
    """ Rotate a path around a given origin using degrees. """
    ox, oy = origin
    new_segments = []
    for segment in path:
        if isinstance(segment, Line):
            start = rotate_point((segment.start.real, segment.start.imag), angle_degrees, origin)
            end = rotate_point((segment.end.real, segment.end.imag), angle_degrees, origin)
            new_segments.append(Line(complex(*start), complex(*end)))
        elif isinstance(segment, CubicBezier):
            start = rotate_point((segment.start.real, segment.start.imag), angle_degrees, origin)
            control1 = rotate_point((segment.control1.real, segment.control1.imag), angle_degrees, origin)
            control2 = rotate_point((segment.control2.real, segment.control2.imag), angle_degrees, origin)
            end = rotate_point((segment.end.real, segment.end.imag), angle_degrees, origin)
            new_segments.append(CubicBezier(complex(*start), complex(*control1), complex(*control2), complex(*end)))
        elif isinstance(segment, QuadraticBezier):
            start = rotate_point((segment.start.real, segment.start.imag), angle_degrees, origin)
            control = rotate_point((segment.control.real, segment.control.imag), angle_degrees, origin)
            end = rotate_point((segment.end.real, segment.end.imag), angle_degrees, origin)
            new_segments.append(QuadraticBezier(complex(*start), complex(*control), complex(*end)))
        elif isinstance(segment, Arc):
            start = rotate_point((segment.start.real, segment.start.imag), angle_degrees, origin)
            end = rotate_point((segment.end.real, segment.end.imag), angle_degrees, origin)
            # Arc rotation may not be fully correct as it does not handle ellipse rotation
            new_segments.append(Arc(complex(*start), segment.radius, segment.rotation, segment.arc, segment.sweep, complex(*end)))
        else:
            raise TypeError("Unsupported segment type")
    return Path(*new_segments)


def transform_svg(svg_file, polygon, dx=0, dy=0, angle=0):
    paths, attributes = svg2paths(svg_file)
    
    polygon = np.array(polygon)
    min_x, max_x = np.min(polygon[:, 0]), np.max(polygon[:, 0])
    min_y, max_y = np.min(polygon[:, 1]), np.max(polygon[:, 1])
    
    poly_width = max_x - min_x
    poly_height = max_y - min_y

    all_x = []
    all_y = []
    for path in paths:
        for segment in path:
            all_x.extend([segment.start.real, segment.end.real])
            all_y.extend([segment.start.imag, segment.end.imag])
    min_svg_x, max_svg_x = min(all_x), max(all_x)
    min_svg_y, max_svg_y = min(all_y), max(all_y)
    svg_width = max_svg_x - min_svg_x
    svg_height = max_svg_y - min_svg_y

    svg_center_x = (min_svg_x + max_svg_x) / 2
    svg_center_y = (min_svg_y + max_svg_y) / 2

    # Apply rotation first
    rotated_paths = [rotate_path(path, angle, origin=(svg_center_x, svg_center_y)) for path in paths]

    # Recalculate bounds after rotation
    all_x_rotated = []
    all_y_rotated = []
    for path in rotated_paths:
        for segment in path:
            all_x_rotated.extend([segment.start.real, segment.end.real])
            all_y_rotated.extend([segment.start.imag, segment.end.imag])
    min_svg_x_rotated, max_svg_x_rotated = min(all_x_rotated), max(all_x_rotated)
    min_svg_y_rotated, max_svg_y_rotated = min(all_y_rotated), max(all_y_rotated)
    
    svg_width_rotated = max_svg_x_rotated - min_svg_x_rotated
    svg_height_rotated = max_svg_y_rotated - min_svg_y_rotated
    svg_center_x_rotated = (min_svg_x_rotated + max_svg_x_rotated) / 2
    svg_center_y_rotated = (min_svg_y_rotated + max_svg_y_rotated) / 2

    # Calculate scale and translation
    scale_x = poly_width / svg_width_rotated
    scale_y = poly_height / svg_height_rotated
    scale = min(scale_x, scale_y)

    poly_center_x = (min_x + max_x) / 2
    poly_center_y = (min_y + max_y) / 2
    
    translate_x = poly_center_x - svg_center_x_rotated * scale
    translate_y = poly_center_y - svg_center_y_rotated * scale

    # Apply translation
    transformed_paths = [translate_path(path, translate_x, translate_y) for path in rotated_paths]
    return transformed_paths, attributes

