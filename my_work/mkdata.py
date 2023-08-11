# -*- coding: utf-8 -*-
import os
import json
from PIL import Image
import random
import shutil

input_folder = "initial_data/train"

output_train_folder = "UAV_dataset/my_train"    #划分的数据集
output_val_folder = "UAV_dataset/my_val"    #划分的验证集
output_test_folder = "UAV_dataset/my_test" #划分的测试集
train_ratio = 0.71  #划分比例

os.makedirs(output_train_folder, exist_ok=True)
os.makedirs(output_val_folder, exist_ok=True)
os.makedirs(output_test_folder, exist_ok=True)

# 遍历所有子文件夹
for sub_folder in os.listdir(input_folder):
    sub_folder_path = os.path.join(input_folder, sub_folder)

    # 获取随机划分的训练家和验证集
    image_file_list = sorted([f for f in os.listdir(sub_folder_path) if f.endswith(".jpg")])
    num_images = len(image_file_list)
    num_train_images = int(num_images * train_ratio)
    num_val_images = (num_images - num_train_images) // 2
    print("all dataset: ",num_images)
    print("train dataset: ",num_train_images)
    print("val dataset and test data set: ",num_val_images,'\n')
    train_indices = random.sample(range(num_images), num_train_images)
    remaining_indices = set(range(num_images)) - set(train_indices)
    val_indices = random.sample(sorted(remaining_indices), num_val_images)
    test_indices = remaining_indices - set(val_indices)

    if not os.path.isdir(sub_folder_path):
        continue

    # 读取IR_label.json
    label_file_path = os.path.join(sub_folder_path, "IR_label.json")
    with open(label_file_path) as f:
        label_data = json.load(f)


    #for i, exist in enumerate(label_data['exist']):
    for i, image_file_name in enumerate(image_file_list):
        input_image_file_path = os.path.join(sub_folder_path, image_file_name)
        if i in train_indices:
            output_image_file_name = f"{sub_folder}_{i+1:06d}.jpg"
            output_image_file_path = os.path.join(output_train_folder, "images", output_image_file_name)
        elif i in val_indices:
            output_image_file_name = f"{sub_folder}_{i+1:06d}.jpg"
            output_image_file_path = os.path.join(output_val_folder, "images", output_image_file_name)
        else:
            output_image_file_name = f"{sub_folder}_{i+1:06d}.jpg"
            output_image_file_path = os.path.join(output_test_folder, "images", output_image_file_name)

        os.makedirs(os.path.dirname(output_image_file_path), exist_ok=True)
        shutil.copy(input_image_file_path, output_image_file_path)

        # 转换为YOLO格式的标签
        if label_data['exist'][i]:
            x, y, w, h = label_data['gt_rect'][i]
            
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
            
            
            if i in train_indices:
                label_file_name = f"{sub_folder}_{i+1:06d}.txt"
                label_file_path = os.path.join(output_train_folder, "labels", label_file_name)
            elif i in val_indices:
                label_file_name = f"{sub_folder}_{i+1:06d}.txt"
                label_file_path = os.path.join(output_val_folder, "labels", label_file_name)
            else:
                label_file_name = f"{sub_folder}_{i+1:06d}.txt"
                label_file_path = os.path.join(output_test_folder, "labels", label_file_name)

            os.makedirs(os.path.dirname(label_file_path), exist_ok=True)
            with open(label_file_path, 'w') as f:
                f.write(label_str)