import numpy as np
import xml.etree.ElementTree as ET

def rotate_point(point, angle, origin):
    """Rotate a point around a given origin using a rotation matrix."""
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    return np.array([qx, qy])

def calculate_centroid(points):
    """Calculate the centroid of a set of points."""
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    _centroid = (sum(x_coords) / len(points), sum(y_coords) / len(points))
    return np.array(_centroid)

def check_and_print_centroid(elem, points, before_or_after):
    """Check and print the centroid of an element before or after transformation."""
    centroid = calculate_centroid(points)
    print(f"Centroid {before_or_after} transformation: {centroid}")
    return centroid

def apply_transform_to_elem(elem, angle, centroid):
    """Apply rotation to an SVG element around its centroid."""
    # Assuming elem points are available in a format that can be directly used
    points = np.array([(float(elem.get('cx', '0')), float(elem.get('cy', '0')))])

    # Print centroid before transformation
    before_centroid = check_and_print_centroid(elem, points, "before")

    # Calculate rotation
    rotated_points = [rotate_point(point, np.radians(angle), before_centroid) for point in points]
    elem.set('cx', str(rotated_points[0][0]))
    elem.set('cy', str(rotated_points[0][1]))

    # Print centroid after transformation to verify
    after_centroid = check_and_print_centroid(elem, rotated_points, "after")

    # Adjust if the centroid has shifted
    if not np.allclose(before_centroid, after_centroid, atol=1e-6):
        correction = before_centroid - after_centroid
        corrected_points = rotated_points + correction
        elem.set('cx', str(corrected_points[0][0]))
        elem.set('cy', str(corrected_points[0][1]))
        print(f"Corrected centroid to: {calculate_centroid(corrected_points)}")

    return elem

# Example usage
elem = ET.Element('circle', {'cx': '100', 'cy': '100', 'r': '50'})
transformed_elem = apply_transform_to_elem(elem, 45, calculate_centroid(np.array([[100, 100]])))
