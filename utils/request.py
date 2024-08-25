from flask import request
import numpy as np
from src import SVGManager, Nester, Object, Material
from .transform import transform_svg_element

def get_request_data():
    """Extract data from the request."""
    data = request.get_json()
    svg_ids = data.get('svg_ids')
    svg_content = data.get('svg_content')
    padding = float(data.get('padding', 0.5))
    return svg_ids, svg_content, padding

def initialize_managers(svg_content):
    """Initialize SVGManager and Nester instances."""
    svgmanager = SVGManager(svg_content)
    
    nester = Nester()
    return svgmanager, nester

def process_svg_element(elem, svgmanager, nester, padding):
    """Process an individual SVG element."""
    if elem.tag.endswith('rect') and elem.attrib.get('target') == 'bin':
        bin_material = Material(
            width=int(float(elem.attrib['width'])),
            height=int(float(elem.attrib['height'])),
            bin_id=elem.attrib.get('id')
        )
        nester.add_material(bin_material)
    else:
        polygon = svgmanager.convert_to_polygon(elem.attrib.get('id'), padding=padding)
        if isinstance(polygon, tuple):
            polygon = np.array(polygon[0]) if len(polygon) == 2 else np.array(polygon)
        if polygon is not None and isinstance(polygon, np.ndarray):
            obj = Object(points=polygon, svg_id=elem.attrib.get('id'))
            nester.add_object(obj)
        else:
            print(f"Failed to process {elem.attrib.get('id')}: polygon is None or invalid.")

def handle_nest_results(nester, svgmanager):
    """Handle the results of the nesting process."""
    for nest_data in nester.nest_result.values():
        if isinstance(nest_data, dict):
            process_nest_data(nest_data, svgmanager)
        else:
            print(f"Unexpected data type for nest_data: {type(nest_data)}")

def process_nest_data(nest_data, svgmanager):
    """Process each nesting result and update the SVG elements accordingly."""
    bin_id = nest_data['material_id']
    area_used = nest_data['area_used']
    object_count = nest_data['objects']

    bin_elem = svgmanager.get_element(bin_id)
    bin_elem.attrib['area'] = f'{area_used:.2f}'
    bin_elem.attrib['objects'] = str(object_count)

    bin_x = float(bin_elem.attrib.get('x', ''))
    bin_y = float(bin_elem.attrib.get('y', ''))

    for svg_id, polygon, rotation in zip(nest_data['svg_ids'], nest_data['vertices_list'], nest_data['rotations']):
        elem = svgmanager.get_element(svg_id)
        transformed_elem = transform_svg_element(
            elem,
            polygon,
            dx=bin_x,
            dy=bin_y,
            angle=rotation
        )
        svgmanager.update_element(svg_id, transformed_elem)

def handle_nesting_request():
    """Main function to handle nesting request."""
    svg_ids, svg_content, padding = get_request_data()
    svgmanager, nester = initialize_managers(svg_content)

    for elem_id in svg_ids:
        elem = svgmanager.get_element(elem_id)
        if elem is None:
            print(f"Element {elem_id} not found.")
            continue
        process_svg_element(elem, svgmanager, nester, padding)

    nester.nest()
    handle_nest_results(nester, svgmanager)

    return svgmanager.get_svg_content()
