from aka_cad import Item, Point
import numpy as np
from utils import get_polygon

class Object:
    def __init__(self, points=None, img_path=""):
        if points is None and img_path:
            points = get_polygon(img_path)
            if points is None:
                raise ValueError("Cannot extract points from image at the provided path.")
            points = [Point(int(x), int(y)) for [x, y] in points]  # Convert kết quả từ get_polygon sang danh sách Point

        elif isinstance(points, np.ndarray):
            # Nếu points là một numpy array, chuyển đổi thành danh sách các điểm
            points = [Point(int(x), int(y)) for [x, y] in points]

        else:
            raise ValueError("Invalid input: must provide a numpy array of points or a valid image path")

        self.item = Item(points)  # Tạo đối tượng Item từ C++
        self.img_path = img_path  # Lưu đường dẫn ảnh nếu có

    def __repr__(self):
        # Cập nhật __repr__ để sử dụng các thuộc tính đã chuyển sang chuỗi từ C++
        return (f"Object(area: {self.area}, bin_id: {self.bin_id}, "
                f"vertices: {self.vertex_count}, translation: {self.translation}, "
                f"rotation: {self.rotation}, img_path: {self.img_path}")

    @property
    def area(self):
        # Lấy diện tích từ đối tượng Item
        return self.item.area

    @property
    def bin_id(self):
        # Lấy ID của bin từ đối tượng Item
        return self.item.bin_id

    @property
    def vertex_count(self):
        # Lấy số lượng đỉnh từ đối tượng Item
        return self.item.vertex_count

    @property
    def translation(self):
        # Đảm bảo translation là một thuộc tính trả về một tuple và không gọi nó như một phương thức
        return self.item.translation  # Chỉ cần truy cập nó như một thuộc tính

    @property
    def rotation(self):
        # Lấy góc xoay, chuyển đổi radian sang độ nếu cần
        return self.item.rotation  # Trả về giá trị radian, convert sang độ nếu muốn

    def vertices(self):
        # Trả về danh sách các đỉnh gốc
        vertices = self.item.raw_vertices()
        return [(x, y) for x, y in vertices]