import cv2
import numpy as np
from svgpathtools import svg2paths
from .transform import sort_points, align_edges

def get_polygon(path, epsilon_ratio=0.02, sort_clockwise=True):
    if path.endswith(".svg"):
        paths, attributes = svg2paths(path)
        max_path = max(paths, key=lambda path: path.length())
        points = np.array([[segment.start.real, segment.start.imag] for segment in max_path] +
                          [[segment.end.real, segment.end.imag] for segment in max_path])
        unique_points = np.unique(points, axis=0)
    else:
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        max_contour = max(contours, key=cv2.contourArea)
        epsilon = epsilon_ratio * cv2.arcLength(max_contour, True)
        unique_points = cv2.approxPolyDP(max_contour, epsilon, True)
        if unique_points is None or unique_points.ndim != 3 or unique_points.shape[1] != 1:
            return None  # Return None if no valid polygon is found
        unique_points = unique_points[:, 0, :]  # Reshape from 3D to 2D array

    # Ensure unique_points is in the correct data type for convexHull
    unique_points = np.array(unique_points, dtype=np.float32)  # Convert to float32

    # Compute the convex hull of the points
    convex_hull = cv2.convexHull(unique_points)

    # Ensure the convex_hull is properly shaped for sorting (remove any extra dimensions)
    if convex_hull.ndim > 2:
        convex_hull = convex_hull.reshape(-1, 2)

    # Sort the points of the convex hull, if necessary
    sorted_points = sort_points(convex_hull, clockwise=sort_clockwise)

    # Align the edges based on the sorted points
    aligned_polygon = align_edges(sorted_points)
    
    return aligned_polygon