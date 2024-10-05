import numpy as np
import cv2
import re
import xml.etree.ElementTree as ET
from PIL import Image
import io
from svgpathtools import parse_path
from utils import sort_points

def rotate_points(points, angle, origin=(0, 0)):
    """Rotate an array of points around a given origin."""
    ox, oy = origin
    cos_angle, sin_angle = np.cos(angle), np.sin(angle)

    return np.array([
        [
            ox + cos_angle * (px - ox) - sin_angle * (py - oy),
            oy + sin_angle * (px - ox) + cos_angle * (py - oy)
        ]
        for px, py in points
    ])

def process_shape(elem, process_func, padding=2):
    """Generic shape processing function."""
    points = process_func(elem)
    return add_padding(compute_convex_hull(points), padding)

def process_ellipse(elem, padding=2):
    """Process an ellipse element."""
    cx, cy = float(elem.attrib['cx']), float(elem.attrib['cy'])
    rx, ry = float(elem.attrib['rx']), float(elem.attrib['ry'])
    theta = np.linspace(0, 2 * np.pi, 15)
    x = cx + (rx +padding + 0.5) * np.cos(theta)
    y = cy + (ry + padding + 0.5) * np.sin(theta)
    points = np.vstack((x, y)).T
    return points

def process_circle(elem, padding=2):
    """Process a circle element."""
    cx, cy = float(elem.attrib['cx']), float(elem.attrib['cy'])
    r = float(elem.attrib['r'])
    theta = np.linspace(0, 2 * np.pi, 15)
    x = cx + (r + padding + 0.5) * np.cos(theta)
    y = cy + (r + padding + 0.5) * np.sin(theta)
    points = np.vstack((x, y)).T
    return points

def process_rect(elem, padding=2):
    """Process a rectangle element."""
    x, y = float(elem.attrib['x']), float(elem.attrib['y'])
    width, height = float(elem.attrib['width']), float(elem.attrib['height'])
    points = np.array([[x, y], [x + width, y], [x + width, y + height], [x, y + height]])
    return process_shape(elem, lambda e: points, padding)

def process_path(elem, padding=2):
    """Process a path element."""
    path_data = elem.attrib.get('d', '')
    if not path_data:
        return None
    path = parse_path(path_data)
    points = np.array([[seg.start.real, seg.start.imag] for seg in path] +
                      [[seg.end.real, seg.end.imag] for seg in path])
    return process_shape(elem, lambda e: points, padding)

def process_line(elem, padding=2):
    """Process a line element."""
    x1, y1 = float(elem.attrib['x1']), float(elem.attrib['y1'])
    x2, y2 = float(elem.attrib['x2']), float(elem.attrib['y2'])
    points = np.array([[x1, y1], [x2, y2]])
    return process_shape(elem, lambda e: points, padding)

def process_polyline(elem, padding=2):
    """Process a polyline element."""
    points = np.array([[float(x), float(y)] for x, y in 
                       [pair.split(',') for pair in elem.attrib['points'].strip().split(' ')]])
    return process_shape(elem, lambda e: points, padding)

def process_polygon(elem, padding=2):
    """Process a polygon element."""
    return process_polyline(elem, padding)

def process_group(elem, padding=2):
    """Process a group of elements and treat them as a single shape with padding."""
    all_points = [
        process_func(child, padding)
        for child, process_func in {
            'ellipse': process_ellipse,
            'circle': process_circle,
            'rect': process_rect,
            'path': process_path,
            'line': process_line,
            'polyline': process_polyline,
            'polygon': process_polygon,
        }.items()
        if child.tag.endswith(process_func.__name__.replace('process_', ''))
    ]
    if all_points:
        combined_points = np.vstack(all_points)
        return add_padding(compute_convex_hull(combined_points), padding)
    return None

def process_complex_shape(elem, padding=2):
    """Convert complex or unsupported elements to an image, find contours, and compute convex hull with padding."""
    svg_str = ET.tostring(elem, encoding='unicode')
    output_width, output_height = 10000, 10000
    png_data = svg2png(bytestring=svg_str, output_width=output_width, output_height=output_height)
    image = Image.open(io.BytesIO(png_data)).convert("L")
    open_cv_image = np.array(image)
    contours, _ = cv2.findContours(open_cv_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
    max_contour = max(contours, key=cv2.contourArea)
    epsilon = 0.02 * cv2.arcLength(max_contour, True)
    approx = cv2.approxPolyDP(max_contour, epsilon, True)
    points = approx[:, 0, :]
    return add_padding(compute_convex_hull(points), padding)

def process_image(elem, padding=2):
    """Convert an SVG image element to a polygon or other format for processing."""
    x = float(elem.attrib.get('x', 0))
    y = float(elem.attrib.get('y', 0))
    width = float(elem.attrib.get('width', 0))
    height = float(elem.attrib.get('height', 0))
    points = np.array([[x, y], [x + width, y], [x + width, y + height], [x, y + height]])
    return add_padding(points, padding) if padding > 0 else points

def compute_convex_hull(points):
    """Compute and sort the convex hull of the polygon."""
    points = np.array(points, dtype=np.float32)
    if len(points) < 3:
        return points
    convex_hull = cv2.convexHull(points).reshape(-1, 2)
    sorted_points = sort_points(convex_hull)
    return np.vstack([sorted_points, sorted_points[0]]) if not np.array_equal(sorted_points[0], sorted_points[-1]) else sorted_points

def add_padding(points, padding=2):
    """Add padding to the polygon, expanding it from its center while keeping the centroid fixed."""
    center = np.mean(points, axis=0)
    directions = points - center
    norms = np.linalg.norm(directions, axis=1, keepdims=True)
    normalized_directions = directions / norms
    expanded_points = center + normalized_directions * (norms + padding)
    return compute_convex_hull(expanded_points)