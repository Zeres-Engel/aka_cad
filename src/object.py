from aka_cad import Item, Point
import numpy as np

class Object:
    def __init__(self, points=None, img_path="", svg_id=""):
        if points is not None:
            if isinstance(points, list) and all(isinstance(p, Point) for p in points):
                self.item = Item(points)
            elif isinstance(points, np.ndarray):
                points = [Point(int(x), int(y)) for [x, y] in points]
                self.item = Item(points)
            else:
                raise ValueError("Invalid input: must provide a list of Point objects or a numpy array of points")
        elif img_path:
            points = get_polygon_from_img(img_path)
            if points is None:
                raise ValueError("Cannot extract points from image at the provided path.")
            points = [Point(int(x), int(y)) for [x, y] in points]
            self.item = Item(points)
        else:
            raise ValueError("Invalid input: must provide a numpy array of points or a valid image path")
        self.img_path = img_path
        self.svg_id = svg_id

    def __repr__(self):
        return (f"Object(area: {self.area}, bin_id: {self.bin_id}, "
                f"vertices: {self.vertex_count}, translation: {self.translation}, "
                f"rotation: {self.rotation}, img_path: {self.img_path}")

    @property
    def area(self):
        return self.item.area

    @property
    def bin_id(self):
        return self.item.bin_id

    @property
    def vertex_count(self):
        return self.item.vertex_count

    @property
    def translation(self):
        return self.item.translation

    @property
    def rotation(self):
        return self.item.rotation
    
    @property
    def item_id(self):
        return self.item.item_id()

    def vertices(self):
        vertices = self.item.raw_vertices()
        return [(x, y) for x, y in vertices]

    def transformed_vertices(self):
        vertices = self.item.transformed_vertices()
        return [(x, y) for x, y in vertices]
