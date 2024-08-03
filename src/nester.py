from .object import Object
from .material import Material
from aka_cad import nest
from utils import export_nest_map, export_raw_svg
import bisect

class Nester:
    def __init__(self):
        self.materials = []  # Danh sách các Materials
        self.objects = []  # Danh sách các Objects, được sắp xếp theo item_id
        self.nest_result = {}  # Từ điển lưu trữ kết quả chuẩn bị dữ liệu

    def add_material(self, material, num_copies=1):
        """Add a pre-configured Material object to the list, optionally multiple copies."""
        if not isinstance(material, Material):
            raise ValueError("Invalid material: Expected a Material object.")
        self.materials.extend([material] * num_copies)  # Thêm bản sao của material vào danh sách

    def add_object(self, obj, num_copies=1):
        """Add an Object instance to the list, sorted by item_id."""
        if not isinstance(obj, Object):
            raise ValueError("Invalid object: Expected an Object instance.")
        for _ in range(num_copies):
            index = bisect.bisect_left([o.item_id for o in self.objects], obj.item_id)
            self.objects.insert(index, obj)

    def nest(self):
        """Nest the objects and update them with the results."""
        items = [obj.item for obj in self.objects]
        nested_result = nest(items, [material.box for material in self.materials])

        self.nest_result = {}
        for index in range(len(self.materials)):
            vertices_list = []
            img_paths = []
            translations = []
            rotations = []

            for obj, item in zip(self.objects, nested_result):
                if int(item.bin_id) == index:
                    vertices_list.append([(x, y) for x, y in item.transformed_vertices()])
                    img_paths.append(obj.img_path)
                    translations.append(item.translation)
                    rotations.append(item.rotation)

            self.nest_result[index] = {
                'vertices_list': vertices_list,
                'img_paths': img_paths,
                'translations': translations,
                'rotations': rotations
            }

    def export_map(self):
        dashed_color = (0, 0, 0)  # Black
        rectangle_color = (17, 105, 176)  # Converted from #1169b0
        poly_color = (255, 112, 29)  # Converted from #ff701d
        for index in self.nest_result:
            data = self.nest_result[index]
            filename = f'map_{index}.png'
            export_nest_map(data['vertices_list'], data['img_paths'], data['translations'], data['rotations'], 
                            self.materials[index], filename, dashed_color=dashed_color, 
                            rectangle_color=rectangle_color, poly_color=poly_color)

    def export_svg(self):
        poly_color = (255, 112, 29)  # Converted from #ff701d
        for index in self.nest_result:
            data = self.nest_result[index]
            filename = f'output/raw_{index}.svg'
            export_raw_svg(data['vertices_list'], data['img_paths'], data['translations'], data['rotations'], 
                           self.materials[index], filename, poly_color=poly_color)

    @property
    def material_dimensions(self):
        return [(m.width, m.height) for m in self.materials]

    @property
    def material_area(self):
        return sum(m.area for m in self.materials)
