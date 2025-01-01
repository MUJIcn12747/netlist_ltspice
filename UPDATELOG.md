# Version:

***Upload Date: 2025/1/1***

## Changed
- parameter.py加入参数Add_Noise控制是否加噪声，同时改动result_analysis、simulate
- formula加了正定和对角占优矩阵的生成函数，data_generator直接调用其中之一
- 映射与网表生成分离，simulate中矩阵映射一次，对应一个输入文本，电压向量输入多次，生成多个网表，正负映射函数在Mapping中，目前只做了inv的
- inv加了条件数计算，输出在matrix_check文本中，以解释误差较大的情况
