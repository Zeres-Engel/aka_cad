import json
import numpy as np
from PIL import Image, ImageDraw

def read_labelme_json(label_path):
    with open(label_path, 'r') as f:
        data = json.load(f)
    return data['shapes']

label_path = '/home/xuanloc/Downloads/CADCAM_project/data/3.json'
label = read_labelme_json(label_path)

img_path = '/home/xuanloc/Downloads/CADCAM_project/data/3.png'
img = Image.open(img_path).convert("RGBA")

for i, obj in enumerate(label):
    obj_name = obj['label']
    obj_poly = [(int(x), int(y)) for x, y in obj['points']]
    
    # Tạo một mask trắng (để sau này dùng làm nền trong suốt)
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).polygon(obj_poly, outline=1, fill=1)
    mask = np.array(mask)

    # Lấy các kênh màu của ảnh gốc
    new_img_array = np.dstack([np.array(img)[..., :-1], mask * 255])
    new_img = Image.fromarray(new_img_array, "RGBA")

    # Crop ảnh theo polygon
    bbox = new_img.getbbox()
    cropped_img = new_img.crop(bbox)
    
    # Lưu ảnh đã crop với nền trong suốt
    output_img_path = f'/home/xuanloc/Downloads/CADCAM_project/data/{obj_name}_{i}.png'
    cropped_img.save(output_img_path)

