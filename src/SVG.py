import xml.etree.ElementTree as ET
import numpy as np
from utils import (
    sort_points, process_circle, process_complex_shape, process_ellipse,
    process_path, process_rect, process_group, compute_convex_hull,
    process_line, process_polyline, process_polygon, add_padding, process_image
)

def strip_svg_namespace(element):
    """Remove namespace from SVG tags."""
    for el in element.iter():
        if '}' in el.tag:
            el.tag = el.tag.split('}', 1)[1]

class SVGManager:
    def __init__(self, content):
        self.tree = ET.ElementTree(ET.fromstring(content))
        self.elements = {}
        self.index_elements()

    def index_elements(self):
        """Index all elements with an ID in the SVG."""
        root = self.tree.getroot()
        strip_svg_namespace(root)
        for elem in root.iter():
            if 'id' in elem.attrib:
                self.elements[elem.attrib['id']] = elem

    def get_element(self, elem_id):
        """Retrieve an element by its ID."""
        return self.elements.get(elem_id)

    def convert_to_polygon(self, elem_id, padding=0):
        """Convert an SVG element to a polygon if possible, applying padding."""
        elem = self.get_element(elem_id)
        if elem is None:
            return None, "Element not found."

        tag = elem.tag.lower()
        if tag == 'circle':
            points = process_circle(elem, padding)
        elif tag == 'ellipse':
            points = process_ellipse(elem, padding)
        elif tag == 'rect':
            points = process_rect(elem, padding)
        elif tag == 'path':
            points = process_path(elem, padding)
        elif tag == 'polygon':
            points = process_polygon(elem, padding)
        elif tag == 'polyline':
            points = process_polyline(elem, padding)
        elif tag == 'line':
            points = process_line(elem, padding)
        elif tag == 'g':
            points = process_group(elem, padding)
        elif tag == 'image':
            points = process_image(elem, padding)
        else:
            return None, "Unsupported element type."

        if points is not None:
            points = compute_convex_hull(points)
            return points, None
        else:
            return None, "Could not process element."

    def update_element(self, elem_id, updated_elem):
        """Update the element in the SVG with the provided updated element."""
        original_elem = self.get_element(elem_id)
        if original_elem is not None:
            original_elem.attrib.update(updated_elem.attrib)
        else:
            print(f"Element with ID {elem_id} not found.")

    def get_svg_content(self):
        """Return the updated SVG content as a plain XML string with the necessary namespace."""
        root = self.tree.getroot()
        
        # Ensure the xmlns attribute is set
        if 'xmlns' not in root.attrib:
            root.set('xmlns', 'http://www.w3.org/2000/svg')
        
        return ET.tostring(root, encoding='unicode', method='xml')
