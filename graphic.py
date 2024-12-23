import os
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

# 设置主目录路径（当前文件夹下的 outputFile 文件夹）
main_folder = os.path.join(os.getcwd(), 'outputFile\mvm')

# 弹出文件夹选择对话框，限制用户只能选择 mvm 或 inv 文件夹
def select_folder():
    root = Tk()
    root.withdraw()  # 隐藏主窗口
    selected_folder = filedialog.askdirectory(initialdir=main_folder, title='Choose mvm or inv or pinv')
    return selected_folder

selected_folder = select_folder()

# 如果用户没有选择文件夹，返回的路径为空
if not selected_folder:
    print('No chosen folder')
else:
    print(f'Chosen folder: {selected_folder}')

# 假设 cmp1, cmp2, ..., cmpN 是子文件夹
cmp_folders = [f for f in os.listdir(selected_folder) if f.startswith('cmp') and os.path.isdir(os.path.join(selected_folder, f))]

# 遍历每个 cmp 文件夹
for cmp_folder in cmp_folders:
    cmp_folder_path = os.path.join(selected_folder, cmp_folder)  # 当前 cmp 文件夹路径
    txt_files = [f for f in os.listdir(cmp_folder_path) if f.endswith('.txt')]  # 找到所有 .txt 文件
    
    # 遍历每个 txt 文件
    for txt_file in txt_files:
        file_path = os.path.join(cmp_folder_path, txt_file)  # 当前 .txt 文件路径
        
        # 打开文件并读取数据
        try:
            with open(file_path, 'r') as f:
                header = f.readline().strip()  # 读取第一行标题（例如 I 和 V）
                data = np.loadtxt(f)  # 按列存储数据
        except Exception as e:
            print(f"无法打开文件: {file_path}. 错误: {e}")
            continue
        
        # 确保数据读取成功
        if data.size == 0:
            print(f"文件 {file_path} 中没有有效数据。")
            continue
        
        # 分割标题为列标题
        header_titles = header.split()
        
        # 提取 I 和 V 数据
        ideal = data[:, 0]  # 第一列为 ideal
        test = data[:, 1]  # 第二列为 test
        
        # 绘制散点图
        plt.figure()
        plt.scatter(ideal, test, label='Data with error', color='blue', marker='o')

        # 添加对称参考线
        min_val = 0  # 原点 (0, 0)
        max_val_x = np.max(ideal)  # ideal 的最大值
        max_val_y = np.max(test)  # test 的最大值
        plt.plot([min_val, max_val_x], [min_val, max_val_y], 'r--', linewidth=1.5)  # 绘制对角线

        # 设置图像属性
        plt.xlabel(header_titles[0])  # 横坐标标签
        plt.ylabel(header_titles[1])  # 纵坐标标签
        plt.title(f'Scatter Plot: {txt_file}')  # 设置标题为文件名
        plt.grid(True)  # 显示网格
        plt.legend()

        # 显示图表
        plt.show()

        # 可选：保存图像到文件
        output_dir = os.path.join(selected_folder, 'output_plots')  # 保存图像的输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)  # 创建目录
        plt.savefig(os.path.join(output_dir, f'{cmp_folder}_{txt_file}.png'))

