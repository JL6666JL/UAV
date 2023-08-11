# -*- coding: utf-8 -*-
import os
import json
from PIL import Image
import random
import shutil

#计算两个box的IOU
def calculate_iou(box1, box2):
    # 提取box1的坐标信息
    x1, y1, w1, h1 = box1

    # 提取box2的坐标信息
    x2, y2, w2, h2 = box2

    # 计算box1的左上角和右下角坐标
    x1_min = x1 - w1 / 2
    y1_min = y1 - h1 / 2
    x1_max = x1 + w1 / 2
    y1_max = y1 + h1 / 2

    # 计算box2的左上角和右下角坐标
    x2_min = x2 - w2 / 2
    y2_min = y2 - h2 / 2
    x2_max = x2 + w2 / 2
    y2_max = y2 + h2 / 2

    # 计算相交部分的坐标
    x_intersection_min = max(x1_min, x2_min)
    y_intersection_min = max(y1_min, y2_min)
    x_intersection_max = min(x1_max, x2_max)
    y_intersection_max = min(y1_max, y2_max)

    # 计算相交部分的宽度和高度
    intersection_width = max(0, x_intersection_max - x_intersection_min)
    intersection_height = max(0, y_intersection_max - y_intersection_min)

    # 计算相交部分的面积
    intersection_area = intersection_width * intersection_height

    # 计算box1和box2的面积
    box1_area = w1 * h1
    box2_area = w2 * h2

    # 计算IOU
    iou = intersection_area / (box1_area + box2_area - intersection_area)
    return iou


def get_all_score():
    images_folder="./ans_test/images"

    ans_labels_folder="./ans_test/labels"
    my_result_folder="./my_result"

    #所有测试图片的列表
    image_file_list = sorted([f for f in os.listdir(images_folder) if f.endswith(".jpg")])

   
    #遍历所有结果
    for one_result in os.listdir(my_result_folder):
        one_result_path=os.path.join(my_result_folder,one_result)
        one_score=0 #本次评分
        T=0 #总帧数
        T_plus=0 #真实标签中有目标的帧数
        sum1=0  #前半部分分子之和
        sum2=0  #后半部分分子之和
        # 遍历所有图片
        for i,image_file_name in enumerate(image_file_list):
            result_file=image_file_name[:-4]+".txt"
            given_result_path=os.path.join(ans_labels_folder,result_file) #给出的结果文件
            my_result_path=os.path.join(one_result_path,result_file)    #我的结果文件
            T+=1
            
            #真实标签存在
            if(os.path.exists(given_result_path)):
                T_plus+=1
                vt=1
            #真实标签不存在
            else:
                vt=0
            #预测标签存在
            if(os.path.exists(my_result_path)):
                pt=0
            #预测标签不存在
            else:
                pt=1
            
            #两个都可见，计算IOU
            if(vt==1 and pt==0):
                with open(given_result_path,'r') as file:
                    given_content=file.read().split(' ')
                # box1=(given_content[1],given_content[2],given_content[3],given_content[4])
                box1=(float(given_content[1]),float(given_content[2]),float(given_content[3]),float(given_content[4]))
                with open(my_result_path,'r') as file:
                    my_content=file.read().split(' ')
                # box2=(my_content[1],my_content[2],my_content[3],my_content[4])
                box2=(float(my_content[1]),float(my_content[2]),float(my_content[3]),float(my_content[4]))
                IOU=calculate_iou(box1,box2)
            else:
                IOU=0
            sum1+=IOU
            if(pt==1 and vt==0):
                sum1+=1
            
            if(pt==1 and vt==1):
                sum2+=1
        
        one_score=sum1/T-0.2*(sum2/T_plus)**0.3
        print("precision: ",one_score)

    
if __name__ == "__main__":
    get_all_score()