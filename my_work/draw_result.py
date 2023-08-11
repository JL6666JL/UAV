# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt

# 创建保存图像的文件夹
os.makedirs('result', exist_ok=True)

# 读取 CSV 文件
data = pd.read_csv('results.csv')

# 获取列标签（第一行的数据）
column_labels = data.columns

# 获取纵坐标数据（除第一列外的其他列）
y_columns = column_labels[1:]

# 绘制折线图并保存
for column in y_columns:
    # 获取横坐标数据（第一列）
    x = data.iloc[:, 0]
    y = data[column]

    plt.plot(x, y)

    # 添加标题和标签
    plt.title(f'Line Chart - {column_labels[0]} vs {column}')
    plt.xlabel(column_labels[0])
    plt.ylabel(column)

    # 替换文件名中的 '/' 为 '_' 并去除前缀空格
    column_name = column.replace('/', '_').strip()

    # 构建保存图像的文件路径
    file_path = os.path.join('result', f'{column_name}_line_chart.png')

    # 保存图像
    plt.savefig(file_path)

    # 清除当前图形以便绘制下一张折线图
    plt.clf()