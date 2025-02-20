import numpy as np

# 初始化参数
N = 16
u = 3.6e4  # 需要根据实际值修改
r1 = 1  # 需要根据实际值修改
r2 = 1  # 需要根据实际值修改

def MVM_Interconnect_R():
    # 初始化矩阵
    X = np.zeros((N, N, 1000))
    Videal = np.zeros((N, N))
    G_ = np.random.rand(N, N)
    G = (1 / u) * G_
    V = 0.2 * np.random.rand(1, N) - 0.1

    # 填充Videal矩阵
    for i in range(N):
        Videal[i, :] = V

    # 初始化D1和D2矩阵
    D1 = np.zeros((N, N))
    D2 = np.zeros((N, N))

    for i in range(N):
        if i == 0:
            D1[0, i] = 1
            D1[1, i] = -1
            D2[0, i] = 2
            D2[1, i] = -1
        elif i == N - 1:
            D1[N - 2, i] = -1
            D1[N - 1, i] = 2
            D2[N - 2, i] = -1
            D2[N - 1, i] = 1
        else:
            D1[i, i] = 2
            D1[i - 1, i] = -1
            D1[i + 1, i] = -1
            D2[i, i] = 2
            D2[i - 1, i] = -1
            D2[i + 1, i] = -1

    # 计算初始状态
    TT = True
    k = 1
    Vtemp = Videal * G

    # 更新矩阵X
    for i in range(999):
        X[:, :, i + 1] = r2 * Vtemp - ((r1 * np.linalg.inv(D2) @ X[:, :, i] + r2 * X[:, :, i] @ np.linalg.inv(D1)) * G)

    # 提取最终结果
    Ideal = X[:, N - 1, 999]

    # 如果需要打印结果，可以输出Ideal
    print(Ideal)

if __name__ == "__main__":
    MVM_Interconnect_R()