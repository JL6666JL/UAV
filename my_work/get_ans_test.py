# -*- coding: utf-8 -*-

import os
import json
import shutil
from PIL import Image

test_folder="initial_data/test"

output_image_folder="ans_test/images"
output_label_folder="ans_test/labels"

os.makedirs(output_image_folder,exist_ok=True)
os.makedirs(output_label_folder,exist_ok=True)


for sub_folder in os.listdir(test_folder):
    sub_folder_path = os.path.join(test_folder,sub_folder)

    if not os.path.isdir(sub_folder_path):
        continue
    image_file_list = sorted([f for f in os.listdir(sub_folder_path) if f.endswith(".jpg")])

    # 读取IR_label.json
    label_file_path = os.path.join(sub_folder_path, "IR_label.json")
    with open(label_file_path) as f:
        label_data = json.load(f)

    for i,image_file_name in enumerate(image_file_list):
        if i==0:
            input_image_file_path = os.path.join(sub_folder_path, image_file_name)
            output_image_file_name = f"{sub_folder}_{i+1:06d}.jpg"
            output_image_file_path = os.path.join(output_image_folder, output_image_file_name)
            os.makedirs(os.path.dirname(output_image_file_path), exist_ok=True)
            shutil.copy(input_image_file_path, output_image_file_path)

            if len(label_data["res"])!=0:
                x, y, w, h = label_data['res'][0]
            
            x_center = x + w / 2
            y_center = y + h / 2
           
            # 读取对应的图片一遍获得图片尺寸
            image_file_name = f"{i+1:06d}.jpg"
            image_file_path = os.path.join(sub_folder_path, image_file_name)
            with Image.open(image_file_path) as img:
                image_width, image_height = img.size
            
            x_norm = x_center / image_width
            y_norm = y_center / image_height
            w_norm = w / image_width
            h_norm = h / image_height
           
            label_str = f"0 {x_norm:.6f} {y_norm:.6f} {w_norm:.6f} {h_norm:.6f}"
            label_file_name = f"{sub_folder}_{i+1:06d}.txt"
            label_file_path = os.path.join(output_label_folder, label_file_name)
            os.makedirs(os.path.dirname(label_file_path), exist_ok=True)
            with open(label_file_path, 'w') as f:
                f.write(label_str)
        else:
            break

