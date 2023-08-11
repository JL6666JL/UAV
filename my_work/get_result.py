# -*- coding: utf-8 -*-
import os
import json
from PIL import Image
import random
import shutil
import json

save_result_folder="./jl_results"
yolo_result_folder="./runs/detect"
images_folder="./initial_data/test"

for one_result in os.listdir(yolo_result_folder):
    if(one_result!=".ipynb_checkpoints"):
        image_path=os.path.join(images_folder,one_result,"000001.jpg")
        with Image.open(image_path) as img:
                image_width, image_height = img.size
        #print(image_width, image_height)
        res=[]
        one_result_path=os.path.join(yolo_result_folder,one_result,'labels')
        images_file_folder=os.path.join(images_folder,one_result)   #对应图片的文件夹
        image_file_list = sorted([f for f in os.listdir(images_file_folder) if f.endswith(".jpg")])

        
        save_path=save_result_folder+"/"+one_result+".txt"
        for i,image_file_name in enumerate(image_file_list):
            #print(txt_file_name)
            txt_file_name=image_file_name[:-4]+".txt"
            txt_path=os.path.join(one_result_path,txt_file_name)
            if(os.path.exists(txt_path)):
                with open(txt_path,'r') as file:
                    now_res=file.readlines()[0].split(' ')
                box=(float(now_res[1]),float(now_res[2]),float(now_res[3]),float(now_res[4]))
                w=round(box[2]*image_width)
                h=round(box[3]*image_height)
                x=round(box[0]*image_height - w/2)
                y=round(box[1]*image_height - h/2)
                res.append([x,y,w,h])
            else:
                res.append([])
            print(i)

        with open(save_path,'w') as file:
            json.dump(res,file)
        with open(save_path,'r') as r:
             origin=r.read()
        with open(save_path,"w") as w:
             w.write("{\"res\": "+origin+"}")

        