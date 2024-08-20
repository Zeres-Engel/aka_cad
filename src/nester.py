from .object import Object
from .material import Material
from aka_cad import nest
import bisect

class Nester:
    def __init__(self):
        self.materials = []
        self.objects = []
        self.nest_result = {}

    def add_material(self, material, num_copies=1):
        if not isinstance(material, Material):
            raise ValueError("Invalid material: Expected a Material object.")
        self.materials.extend([material] * num_copies)

    def add_object(self, obj, num_copies=1):
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
        for index, material in enumerate(self.materials):
            vertices_list = []
            img_paths = []
            translations = []
            rotations = []
            svg_ids = []

            for obj, item in zip(self.objects, nested_result):
                if int(item.bin_id) == index:
                    vertices_list.append([(x, y) for x, y in item.transformed_vertices()])
                    img_paths.append(obj.img_path)
                    translations.append(item.translation)
                    rotations.append(item.rotation)
                    svg_ids.append(obj.svg_id)

            self.nest_result[index] = {
                'material_id': material.bin_id,
                'vertices_list': vertices_list,
                'img_paths': img_paths,
                'translations': translations,
                'rotations': rotations,
                'svg_ids': svg_ids
            }

    @property
    def material_dimensions(self):
        return [(m.width, m.height) for m in self.materials]

    @property
    def material_area(self):
        return sum(m.area for m in self.materials)
