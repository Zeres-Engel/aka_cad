from flask import request
import numpy as np
from src import SVGManager, Nester, Object, Material
from .transform import transform_svg_element, transform_rotation

def handle_nesting_request():
    data = request.get_json()
    svg_ids = data.get('svg_ids')
    svg_content = data.get('svg_content')
    padding = float(data.get('padding', 0.2))

    # Initialize SVGManager and Nester
    svgmanager = SVGManager(svg_content)
    nester = Nester()

    # Process each SVG element
    for elem_id in svg_ids:
        elem = svgmanager.get_element(elem_id)
        if elem is None:
            print(f"Element {elem_id} not found.")
            continue
        
        # Handle bin elements
        if elem.tag.endswith('rect') and elem.attrib.get('target') == 'bin':
            bin_material = Material(
                width=int(float(elem.attrib['width'])),
                height=int(float(elem.attrib['height'])),
                bin_id=elem_id
            )
            nester.add_material(bin_material)
        else:
            polygon = svgmanager.convert_to_polygon(elem_id, padding=padding)
            if isinstance(polygon, tuple):
                polygon = np.array(polygon[0]) if len(polygon) == 2 else np.array(polygon)
            if polygon is not None and isinstance(polygon, np.ndarray):
                obj = Object(points=polygon, svg_id=elem_id)
                nester.add_object(obj)
            else:
                print(f"Failed to process {elem_id}: polygon is None or invalid.")
    
    nester.nest()

    # Process nest results
    for nest_data in nester.nest_result.values():
        if isinstance(nest_data, dict):
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
                transformed_elem = transform_rotation(transformed_elem, bin_elem)
                svgmanager.update_element(svg_id, transformed_elem)
        else:
            print(f"Unexpected data type for nest_data: {type(nest_data)}")

    return svgmanager.get_svg_content()
