import cv2
import numpy as np
# from aka_cad import Point, Item, Box, nest, SVGWriter
from utils import get_polygon_from_img, get_polygon_from_svg


def add_objs(polygon, items, scale_factor=20000, num_copies=1):
    for i in range(num_copies):
        points = [Point(int(x * scale_factor), int(y * scale_factor)) for [x, y] in polygon]
        for [x, y] in polygon:
            print([x, y])
        print("----------------------------")
        item = Item(points)
        items.append(item)

def main():
    input_items = []
    add_objs(get_polygon_from_img('/app/aka_cad/data/obj1.png'), input_items, scale_factor=200000, num_copies=5)
    add_objs(get_polygon_from_img('/app/aka_cad/data/obj4_0.png'), input_items, scale_factor=200000, num_copies=5)
    add_objs(get_polygon_from_img('/app/aka_cad/data/obj3.png'), input_items, scale_factor=200000, num_copies=6)
    add_objs(get_polygon_from_img('/app/aka_cad/data/obj2.png'), input_items, scale_factor=200000, num_copies=8)

    material_box = Box(150000000, 150000000)
    
    pgrp = nest(input_items, material_box)
    
    sw = SVGWriter()
    sw.write_packgroup(pgrp)
    sw.save()

if __name__ == "__main__":
    # main()
    print(get_polygon_from_svg('data\obj1.svg'))
