# -*- coding: utf-8 -*-

import os
import pandas as pd
import matplotlib.pyplot as plt

# ��������ͼ����ļ���
os.makedirs('result', exist_ok=True)

# ��ȡ CSV �ļ�
data = pd.read_csv('results.csv')

# ��ȡ�б�ǩ����һ�е����ݣ�
column_labels = data.columns

# ��ȡ���������ݣ�����һ����������У�
y_columns = column_labels[1:]

# ��������ͼ������
for column in y_columns:
    # ��ȡ���������ݣ���һ�У�
    x = data.iloc[:, 0]
    y = data[column]

    plt.plot(x, y)

    # ��ӱ���ͱ�ǩ
    plt.title(f'Line Chart - {column_labels[0]} vs {column}')
    plt.xlabel(column_labels[0])
    plt.ylabel(column)

    # �滻�ļ����е� '/' Ϊ '_' ��ȥ��ǰ׺�ո�
    column_name = column.replace('/', '_').strip()

    # ��������ͼ����ļ�·��
    file_path = os.path.join('result', f'{column_name}_line_chart.png')

    # ����ͼ��
    plt.savefig(file_path)

    # �����ǰͼ���Ա������һ������ͼ
    plt.clf()