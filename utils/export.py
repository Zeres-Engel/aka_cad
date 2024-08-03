import numpy as np
import cv2
import os
import svgwrite
from .transform import transform_svg
from .draw_poly import draw_dashed_polygon, create_canvas, add_padding, draw_rectangle, draw_svg_on_canvas, create_svg_canvas, draw_svg_on_svg_canvas

def export_nest_map(vertices_list, img_paths, translations, rotations, material, filename="output.png",
                    max_resolution=1000, padding=10, dashed_color=(0, 0, 0), rectangle_color=(17, 105, 176), poly_color=(255, 112, 29)):
    canvas = create_canvas(int(material.width), int(material.height), color=(255, 255, 255))
    for vertices, img_path, translation, rotation in zip(vertices_list, img_paths, translations, rotations):
        if img_path and img_path.endswith('.svg'):
            transformed_paths, attributes = transform_svg(img_path, vertices, dx=translation[0], dy=translation[1], angle=rotation)
            draw_svg_on_canvas(transformed_paths, canvas, position=(0, 0), color=poly_color)
        if len(vertices) > 0:
            draw_dashed_polygon(canvas, vertices, color=dashed_color, thickness=2)
    draw_rectangle(canvas, (0, 0), (int(material.width) - 1, int(material.height) - 1), color=rectangle_color, thickness=2)
    padded_canvas = add_padding(canvas, padding, color=(255, 255, 255))
    max_side = max(padded_canvas.shape[1], padded_canvas.shape[0])
    scale_factor = max_resolution / max_side
    resized_image = cv2.resize(padded_canvas, (int(padded_canvas.shape[1] * scale_factor), int(padded_canvas.shape[0] * scale_factor)), interpolation=cv2.INTER_AREA)
    cv2.imwrite(filename, resized_image)
    print(f"Exported {filename}")
    
def rgb_to_hex(rgb):
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

def export_raw_svg(vertices_list, img_paths, translations, rotations, material, filename="output.svg", poly_color=(255, 112, 29)):
    poly_color_hex = rgb_to_hex(poly_color)  # Chuyển màu RGB sang Hex
    dwg = create_svg_canvas(int(material.width), int(material.height))
    for vertices, img_path, translation, rotation in zip(vertices_list, img_paths, translations, rotations):
        if img_path and img_path.endswith('.svg'):
            transformed_paths, attributes = transform_svg(img_path, vertices, dx=translation[0], dy=translation[1], angle=rotation)
            draw_svg_on_svg_canvas(transformed_paths, dwg, position=(0, 0), stroke_color=poly_color_hex)
    dwg.saveas(filename)
    print(f"Exported {filename}")
    
def get_next_filename(prefix, ext, directory="."):
    # Kiểm tra các file đã tồn tại với prefix
    existing_files = [f for f in os.listdir(directory) if f.startswith(prefix) and f.endswith(ext)]
    existing_numbers = [int(f[len(prefix):-len(ext)]) for f in existing_files if f[len(prefix):-len(ext)].isdigit()]
    next_number = max(existing_numbers, default=0) + 1
    return f"{prefix}{next_number}{ext}"
    
def export_polygons_to_svg(polygons, output_prefix="obj", poly_color=(255, 112, 29), directory="/data/objects"):
    poly_color_hex = rgb_to_hex(poly_color)  # Chuyển màu RGB sang Hex
    paths = []
    
    for i, polygon in enumerate(polygons, start=1):
        filename = get_next_filename(output_prefix, ".svg", directory)
        dwg = create_svg_canvas(1000, 1000)  # Tạo canvas SVG với kích thước mặc định (bạn có thể điều chỉnh)
        path_data = "M" + " L".join([f"{x},{y}" for x, y in polygon]) + " Z"
        dwg.add(dwg.path(d=path_data, fill='none', stroke=poly_color_hex, stroke_width=2))
        dwg.saveas(os.path.join(directory, filename))
        paths.append(os.path.join(directory, filename))
        print(f"Exported {filename}")
    
    return paths