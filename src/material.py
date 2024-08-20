import cv2
from aka_cad import Box

class Material:
    def __init__(self, width=None, height=None, img_path=None, bin_id=""):
        if img_path and (width is None or height is None):
            dimensions = self.extract_dimensions_from_image(img_path)
            if dimensions:
                width, height = dimensions
            else:
                raise ValueError("Could not extract dimensions from image and no dimensions provided")

        if width is None or height is None:
            raise ValueError("Width and height must be provided")

        self.box = Box(width, height)
        self.bin_id = bin_id

    def __repr__(self):
        return f"Material(width: {self.width}, height: {self.height})"

    @property
    def width(self):
        return self.box.width()

    @property
    def height(self):
        return self.box.height()

    @property
    def area(self):
        return self.box.area()

    def extract_dimensions_from_image(self, img_path):
        try:
            image = cv2.imread(img_path)
            if image is None:
                return None
            height, width, _ = image.shape
            return (width, height)
        except Exception as e:
            print(f"Error reading image dimensions: {str(e)}")
            return None
