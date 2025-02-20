import numpy as np
import os
from parameters import NUM_MATRIX, NUM_I, NoiseModel_or_NoiseSource, Add_Noise
from formula import Calculate_Relative_Error

def process_file(file_name):
    # 读取数据文件并计算相对误差
    data = np.loadtxt(file_name, skiprows=1)  # 跳过第一行标题
    I_ideal = data[:, 0]  # 第一列为Iideal
    I_test = data[:, 1]   # 第二列为Itest

    # 计算相对误差
    relative_errors = Calculate_Relative_Error(I_ideal, I_test)
    return relative_errors

def clear_file(file_name):
    # 清除文件内容
    with open(file_name, 'w') as f:
        pass

def save_relative_error(output_folder, j, relative_errors):
    # 保存计算出的相对误差到输出文件夹
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, f"{j}.txt")
    # clear_file(output_file)
    with open(output_file, 'a') as f:
        f.write(f"{relative_errors}\n")

def Evaluation():
    base_input_folder = r"outputFile\inv"
    if Add_Noise and NoiseModel_or_NoiseSource:
        output_folder = r"NoiseTran\Model"
    elif Add_Noise:
        output_folder = r"NoiseTran\Source"
    else:
        output_folder = r"NoiseTran\Original"

    # clear_file('a.txt')
    j = 1  # 记录输出文件的编号
    for k in range(1, NUM_MATRIX + 1):
        cmp_folder = os.path.join(base_input_folder, f"cmp{k}")
        
        # 读取cmp{k}文件夹中的所有文本文件
        for i in range(1, NUM_I + 1):
            file_name = os.path.join(cmp_folder, f"{i}.txt")
            
            # 检查文件是否存在
            if os.path.exists(file_name):
                relative_errors = process_file(file_name)
                save_relative_error(output_folder, j, relative_errors)
                print(f"已处理文件: {file_name}, 结果保存为 {j}.txt")
                j += 1  # 增加输出文件编号

if __name__ == "__main__":
    Evaluation()
