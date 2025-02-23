import numpy as np
import time
from parameters import WireResistance, ROW_MVM, COL_MVM

def MVM_IRdrop(N, M, V_in, G, tolerance, max_iterations):
    V_ideal = np.tile(V_in, (N, 1))
    # print(V_in)
    # print(V_ideal)

    U = np.full((N, M), 1e-10)
    # print(U)

    r1 = WireResistance  
    r2 = WireResistance

    D1 = np.zeros((N, N))
    D2 = np.zeros((M, M))
    for i in range(N):
        if i == 0:
            D1[0, i] = 2
            D1[1, i] = -1
        elif i == N - 1:
            D1[N - 2, i] = -1
            D1[N - 1, i] = 1
        else:
            D1[i, i] = 2
            D1[i - 1, i] = -1
            D1[i + 1, i] = -1

    for i in range(M):
        if i == 0:
            D2[0, i] = 1
            D2[1, i] = -1
        elif i == M - 1:
            D2[M - 2, i] = -1
            D2[M - 1, i] = 2
        else:
            D2[i, i] = 2
            D2[i - 1, i] = -1
            D2[i + 1, i] = -1

    S=time.time()
    for k in range(max_iterations):
        U_new = (r2 * G * (V_ideal - r1 / r2 * np.linalg.inv(D1) @ U @ D2 - U)) @ np.linalg.inv(D2)

        if np.linalg.norm(U_new - U) < tolerance:
            E=time.time()
            print(f"Converges in the {k+1}th iteration. Runtime: ", E-S)
            # print('Runtime: ', E-S)
            return U_new[:, M-1] / r2
        U = U_new

    print("未收敛")
    return None

if __name__ == "__main__":
    N = ROW_MVM
    M = COL_MVM
    V_in = 0.2 * np.random.rand(N) - 0.1
    u = 3.6e4
    G_ = np.random.rand(N, M)
    G = (1 / u) * G_
    # print(G)
    I = MVM_IRdrop(N, V_in.copy(), G.copy(), 1e-6, 1000)
    print(G @ V_in)
    print(I)