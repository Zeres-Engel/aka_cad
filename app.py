from flask import Flask, render_template, request, jsonify
import numpy as np
from src import SVGManager, Object, Material, Nester
from utils import transform_svg_element, transform_rotation

app = Flask(__name__, static_folder='app/static', template_folder='app/templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nest', methods=['POST'])
def nest():
    data = request.get_json()
    svg_ids = data.get('svg_ids')
    print(svg_ids)
    svg_content = data.get('svg_content')
    
    # Initialize SVGManager and Nester
    svgmanager = SVGManager(svg_content)
    nester = Nester()

    # Process each SVG element
    for elem_id in svg_ids:
        print(elem_id)
        elem = svgmanager.get_element(elem_id)
        if elem is None:
            print(f"Element {elem_id} not found.")
            continue
        
        # Handle bin elements
        if elem.tag.endswith('rect') and elem.attrib.get('target') == 'bin':
            bin_material = Material(width=int(float(elem.attrib['width'])), height=int(float(elem.attrib['height'])), bin_id=elem_id)
            nester.add_material(bin_material)
        else:
            polygon = svgmanager.convert_to_polygon(elem_id, padding=0.2)
            if isinstance(polygon, tuple):
                polygon = np.array(polygon[0]) if len(polygon) == 2 else np.array(polygon)
            if polygon is not None and isinstance(polygon, np.ndarray):
                print(f"Processing {elem_id} with polygon shape {polygon.shape}")
                obj = Object(points=polygon, svg_id=elem_id)
                nester.add_object(obj)
            else:
                print(f"Failed to process {elem_id}: polygon is None or invalid.")
    
    nester.nest()
    for index, nest_data in nester.nest_result.items():
        if isinstance(nest_data, dict):
            bin_id = nest_data['material_id']
            bin_elem = svgmanager.get_element(bin_id)
            bin_x = float(bin_elem.attrib.get('x', ''))
            bin_y = float(bin_elem.attrib.get('y', ''))
            
            for svg_id, polygon, translation, rotation in zip(nest_data['svg_ids'], nest_data['vertices_list'], nest_data['translations'], nest_data['rotations']):
                elem = svgmanager.get_element(svg_id)                                                

                dx, dy = translation
                transformed_elem = transform_svg_element(
                    elem,
                    polygon=polygon,
                    dx=dx + bin_x,
                    dy=dy + bin_y,
                    angle=rotation
                )
                transformed_elem = transform_rotation(transformed_elem, bin_elem)
                svgmanager.update_element(svg_id, transformed_elem)
        else:
            print(f"Unexpected data type for nest_data at index {index}: {type(nest_data)}")

    # Generate updated SVG content
    new_svg_content = svgmanager.get_svg_content()
    # Save the updated SVG content to a file
    with open('updated_output.svg', 'w') as file:
        file.write(new_svg_content)

    return jsonify({
        'new_svg_content': new_svg_content
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
