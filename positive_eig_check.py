import numpy as np

def check_positive_real_eigenvalues(matrix):
    try:
        # 计算特征值
        eigenvalues = np.linalg.eigvals(matrix)

        #print(eigenvalues)

        # 检查实部是否全为正
        result = np.all(np.real(eigenvalues) > 0)
        return eigenvalues, result

        # if result:
        #     print("所有特征值的实部都为正。")
        #     return eigenvalues, result
        # else:
        #     print("存在特征值的实部不为正。")
        #     return eigenvalues, result

    except np.linalg.LinAlgError as e:
        print(f"矩阵特征值计算失败: {e}")
        return False

if __name__ == "__main__":
    # 示例矩阵
    matrix = np.array([[2, -1],
                       [-1, 2]])

    # 检查特征值实部是否全为正
    result = check_positive_real_eigenvalues(matrix)

    if result:
        print("所有特征值的实部都为正。")
    else:
        print("存在特征值的实部不为正。")
