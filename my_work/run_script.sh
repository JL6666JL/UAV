#!/bin/bash

# 获取 ./runs/detect/train6/weights/ 目录下除了 best.pt 和 last.pt 之外的所有 .pt 文件
for file in ./runs/detect/train6/epoch_weights/*.pt; do
    filename=$(basename "$file")
    if [[ $filename != "best.pt" && $filename != "last.pt" ]]; then
        echo "Processing file: $file"
        yolo task=detect mode=predict model="$file" save_txt=true source=/root/autodl-tmp/ans_test/images/ save=false
    fi
done