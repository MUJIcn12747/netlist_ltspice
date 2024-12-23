import numpy as np
from formula import Calculate_diag_matrixU

def check_positive_real_eigenvalues(matrix_A):
    try:
        # calculate eigenvalues of M = UA
        matrix_U = Calculate_diag_matrixU(matrix_A)
        matrix_M = np.dot(matrix_U, matrix_A)
        eigenvalues = np.linalg.eigvals(matrix_M)

        # print(eigenvalues)
        # print(matrix_M)

        # The real parts of all eigenvalues are positive or not
        result = np.all(np.real(eigenvalues) > 0)
        return eigenvalues, result

    except np.linalg.LinAlgError as e:
        print(f"Calculating eigenvalues failed: {e}")
        return False

if __name__ == "__main__":
    # 示例矩阵
    matrix = np.array([[2, -1],
                       [-1, 2]])

    # 检查特征值实部是否全为正
    eigenvalues, result = check_positive_real_eigenvalues(matrix)

    if result:
        print(eigenvalues)
        print("所有特征值的实部都为正。")
    else:
        print(eigenvalues)
        print("存在特征值的实部不为正。")
