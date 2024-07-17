from .object import Object
from .material import Material
from aka_cad import nest
from utils import export_nest_map, export_raw_svg

class Nester:
    def __init__(self):
        self.materials = []  # Danh sách các Materials
        self.objects = []  # Danh sách các Objects
        self.nested_items = []  # Chỗ chứa kết quả sau khi các items được nest

    def add_material(self, material, num_copies=1):
        """Add a pre-configured Material object to the list, optionally multiple copies."""
        if not isinstance(material, Material):
            raise ValueError("Invalid material: Expected a Material object.")
        self.materials.extend([material] * num_copies)  # Thêm bản sao của material vào danh sách


    def add_object(self, obj, num_copies=1):
        if not isinstance(obj, Object):
            raise ValueError("Invalid object: Expected an Object instance.")
        self.objects.extend([obj] * num_copies)  # Sử dụng list multiplication để thêm bản sao

    def nest(self):
        """Nest the objects and update the nested_items list with the results."""
        # Lấy kết quả nested, giả sử thứ tự các Item giống như khi được gửi đi
        nested_result = nest([obj.item for obj in self.objects], [material.box for material in self.materials])
        self.nested_items = nested_result  # Lưu kết quả vào nested_items

        if len(self.nested_items) != len(self.objects):
            print("Warning: The number of items returned does not match the number of objects.")
            return

    def export_map(self):
        dashed_color = (0, 0, 0)  # Black
        rectangle_color = (17, 105, 176)  # Converted from #1169b0
        poly_color = (255, 112, 29)  # Converted from #ff701d
        for index, material in enumerate(self.materials):
            vertices_list, img_paths, translations, rotations = self.prepare_export_data(index)
            filename = f'map_{index}.png'
            export_nest_map(vertices_list, img_paths, translations, rotations, material, filename,
                            dashed_color=dashed_color, rectangle_color=rectangle_color, poly_color=poly_color)

    def export_svg(self):
        poly_color = (255, 112, 29)  # Converted from #ff701d
        for index, material in enumerate(self.materials):
            vertices_list, img_paths, translations, rotations = self.prepare_export_data(index)
            filename = f'raw_{index}.svg'
            export_raw_svg(vertices_list, img_paths, translations, rotations, material, filename, poly_color=poly_color)

    def prepare_export_data(self, material_index):
        vertices_list = []
        img_paths = []
        translations = []
        rotations = []
        for item, obj in zip(self.nested_items, self.objects):
            if int(item.bin_id) == material_index:
                vertices_list.append([(x, y) for x, y in item.transformed_vertices()])
                img_paths.append(obj.img_path)
                translations.append(item.translation)
                rotations.append(item.rotation)
        return vertices_list, img_paths, translations, rotations
    @property
    def material_dimensions(self):
        return [(m.width, m.height) for m in self.materials]

    @property
    def material_area(self):
        return sum(m.area for m in self.materials)
