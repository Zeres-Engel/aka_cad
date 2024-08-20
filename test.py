from src import SVGManager, Nester, Object, Material
from utils import transform_svg_element, transform_rotation
import numpy as np

# Initialize SVGManager and Nester with provided SVG content
svg_content = '''
<svg width="800" height="600">

 <g>
  <title>Layer 1</title>
  <ellipse ry="34" rx="31.5" id="svg_1" cy="114.99999" cx="174.09999" stroke="#000" fill="#fff" />
  <rect id="svg_2" height="66" width="46" y="90.99999" x="271.59999" stroke="#000" fill="#fff" />
  <rect id="svg_3" height="105" width="70" y="74.99999" x="386.59999" stroke="#000" fill="#fff" />
  <rect id="svg_4" height="100" width="34" y="167.99999" x="342.59999" stroke="#000" fill="#fff" />
  <rect area="100" objects="0" nesters="1" machine="100" target="bin" id="svg_5" height="188" width="377.99999" y="283.99999" x="101.59999" stroke="#000" fill="#f0ad4e" />
 </g>
</svg>
'''

# Initialize SVGManager and Nester
svgmanager = SVGManager(svg_content)
nester = Nester()

# Nest elements
svg_ids = ['svg_1', 'svg_2', 'svg_3', 'svg_4', 'svg_5']
for elem_id in svg_ids:
    elem = svgmanager.get_element(elem_id)
    if elem is None:
        print(f"Element {elem_id} not found.")
        continue
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

# Perform nesting
nester.nest()

# Apply transformations and update SVG elements based on the nest result
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

# Output the updated SVG content
updated_svg_content = svgmanager.get_svg_content()

# Save the updated SVG content to a file
with open('updated_output.svg', 'w') as file:
    file.write(updated_svg_content)

print("SVG file has been updated and saved as 'updated_output.svg'.")
