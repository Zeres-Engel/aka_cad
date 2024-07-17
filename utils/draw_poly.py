import cv2
import numpy as np
import svgwrite
from svgpathtools import svg2paths, Path, Line

def draw_dashed_polygon(img, points, color, thickness=2, line_type=cv2.LINE_8, dash_length=10, gap_length=5):
    points = np.array(points, np.int32).reshape((-1, 1, 2))
    num_points = len(points)
    for i in range(num_points):
        p1 = tuple(points[i][0])
        p2 = tuple(points[(i + 1) % num_points][0])
        
        # Draw dashed line between points p1 and p2
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        distance = np.sqrt(dx**2 + dy**2)
        if distance == 0:
            continue
        
        dash_num = int(distance / (dash_length + gap_length))
        for n in range(dash_num + 1):  # +1 to make sure it covers all segments
            start = n * (dash_length + gap_length)
            end = start + dash_length
            if start < distance:
                start_frac = start / distance
                end_frac = min(end / distance, 1)
                start_dash = (int(p1[0] + start_frac * dx), int(p1[1] + start_frac * dy))
                end_dash = (int(p1[0] + end_frac * dx), int(p1[1] + end_frac * dy))
                cv2.line(img, start_dash, end_dash, color, thickness, line_type)
                
def create_canvas(width, height, color=(255, 255, 255)):
    canvas = np.full((height, width, 3), color, dtype=np.uint8)
    return canvas

def add_padding(img, padding, color=(255, 255, 255)):
    height, width = img.shape[:2]
    padded_canvas = create_canvas(width + 2 * padding, height + 2 * padding, color)
    padded_canvas[padding:padding + height, padding:padding + width] = img
    return padded_canvas

def draw_rectangle(img, top_left, bottom_right, color=(17, 105, 176), thickness=2, line_type=cv2.LINE_8):
    cv2.rectangle(img, top_left, bottom_right, color, thickness=thickness, lineType=line_type)
    cv2.GaussianBlur(img, (5, 5), 0)  # Apply Gaussian blur

def draw_svg_on_canvas(paths, canvas, position=(0, 0), scale=1.0, color=(255, 112, 29)):
    for path in paths:
        for segment in path:
            start_point = (int(segment.start.real * scale + position[0]), int(segment.start.imag * scale + position[1]))
            end_point = (int(segment.end.real * scale + position[0]), int(segment.end.imag * scale + position[1]))
            cv2.line(canvas, start_point, end_point, color, 2)

def draw_dashed_lines(dwg, vertices, dash_length=10, gap_length=5):
    """Draw dashed lines given a list of vertices."""
    num_vertices = len(vertices)
    if num_vertices < 2:
        return  # Not enough points to draw a line
    
    for i in range(num_vertices - 1):
        start_point = vertices[i]
        end_point = vertices[i + 1]
        dx, dy = end_point[0] - start_point[0], end_point[1] - start_point[1]
        distance = (dx**2 + dy**2)**0.5
        num_dashes = int(distance // (dash_length + gap_length))
        for j in range(num_dashes):
            line_start = (start_point[0] + j * (dash_length + gap_length) * dx / distance,
                          start_point[1] + j * (dash_length + gap_length) * dy / distance)
            line_end = (line_start[0] + dash_length * dx / distance,
                        line_start[1] + dash_length * dy / distance)
            dwg.add(dwg.line(line_start, line_end, stroke=svgwrite.rgb(10, 10, 16, '%'), stroke_width=2))

def create_svg_canvas(width, height):
    """Create a new SVG canvas."""
    return svgwrite.Drawing(size=(width, height))

def draw_rectangle_svg(dwg, top_left, bottom_right, color="red", thickness=2):
    dwg.add(dwg.rect(insert=top_left, size=(bottom_right[0] - top_left[0], bottom_right[1] - top_left[1]),
                     stroke=color, fill="none", stroke_width=thickness))

def draw_svg_on_svg_canvas(paths, dwg, position=(0, 0), scale=1.0, stroke_color="blue"):
    for path in paths:
        for segment in path:
            start_point = (segment.start.real * scale + position[0], segment.start.imag * scale + position[1])
            end_point = (segment.end.real * scale + position[0], segment.end.imag * scale + position[1])
            dwg.add(dwg.line(start=start_point, end=end_point, stroke=stroke_color, stroke_width=2))



