import cv2
import numpy as np
from svgpathtools import svg2paths

def sort_points_clockwise(points):
    """ Sort the points of the polygon in clockwise order and ensure the start point is also the end point. """
    if points.size == 0:
        return points
    # Reshape points to ensure it's in the correct format
    points = points.reshape(-1, 2)
    centroid = np.mean(points, axis=0)
    angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])
    sorted_points = points[np.argsort(-angles)]
    if not np.array_equal(sorted_points[0], sorted_points[-1]):
        sorted_points = np.vstack([sorted_points, sorted_points[0:1]])
    return sorted_points.astype(int)  # Cast to int

def align_edges(polygon, threshold_angle=3):
    """ Align edges to make them more horizontal or vertical based on a threshold angle. """
    if polygon is None:
        return None
    new_polygon = np.copy(polygon)
    num_points = len(polygon) - 1

    for i in range(num_points):
        p1 = polygon[i]
        p2 = polygon[i + 1]
        
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        
        angle = np.degrees(np.arctan2(dy, dx))
        angle = abs(angle) % 180
        if angle <= threshold_angle or angle >= (180 - threshold_angle):
            new_polygon[i + 1][1] = new_polygon[i][1]
        elif (angle >= (90 - threshold_angle)) and (angle <= (90 + threshold_angle)):
            new_polygon[i + 1][0] = new_polygon[i][0]

    return new_polygon.astype(int)  # Cast to int

def get_polygon_from_img(image_path, epsilon_ratio=0.02):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None

    max_contour = max(contours, key=cv2.contourArea)
    epsilon = epsilon_ratio * cv2.arcLength(max_contour, True)
    approx = cv2.approxPolyDP(max_contour, epsilon, True)
    sorted_approx = sort_points_clockwise(approx)
    aligned_contour = align_edges(sorted_approx)

    return aligned_contour  # Return without centering

def get_polygon_from_svg(svg_path):
    paths, attributes = svg2paths(svg_path)
    
    # Select the largest path (modify as needed)
    max_path = max(paths, key=lambda path: path.length())
    
    # Extract points from the path
    points = []
    for segment in max_path:
        points.append([segment.start.real, segment.start.imag])
        points.append([segment.end.real, segment.end.imag])
    
    # Remove duplicate points and sort them clockwise
    unique_points = np.unique(np.array(points), axis=0)
    sorted_points = sort_points_clockwise(unique_points)
    
    return sorted_points  # Return without modifications to type

