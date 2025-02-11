import numpy as np
from device import RRAM_
from parameters import maxConductance, minConductance, AM_or_QM, error_range_AM, num_Bit, sigma_QW, unit_Current, unit_Voltage, alpha_inv

def Array_RealDevice_Update(A, N, M):
    A_actual = np.zeros_like(A)
    max_value = np.max(A)
    min_value = np.min(A)
    rram = RRAM_(maxConductance, minConductance, AM_or_QM, error_range_AM, num_Bit, sigma_QW)
    for i in range(N):
        for j in range(M):
            # 对每个元素应用 Write 函数
            A_actual[i, j] = rram.Write(A[i, j], max_value, min_value)
    # print(A_actual)
    return A_actual

def InputVector_to_InputVoltage(vector_b):
    Voltage = (-1) * vector_b * alpha_inv / np.max(vector_b)
    return Voltage

def Mapping_inv_pos(N, A):
    G_actual = Array_RealDevice_Update(A,N,N)       # attach device model to conductance
    A_actual = G_actual / maxConductance
    R = 1 / G_actual                   # convert conductance to resistance
    R2 = np.zeros_like(R)
    
    return A_actual, R, R2

def Mapping_inv_neg(N, A):
    A2=A.copy()
    for i in range(N):
        for j in range(N):
            if (A[i][j]>0):
                A[i][j]=A[i][j]*2
                A2[i][j]=A[i][j]/2
            else:
                A[i][j]=-A[i][j]
                A2[i][j]=A[i][j]*2
    A_combined=np.vstack((A,A2))
    '''
    g_min=np.min(A_combined)
    g_max=np.max(A_combined)
    if (g_max/g_min>10):
        A_combined=A_combined+g_max/9
    '''
    G_actual = Array_RealDevice_Update(A_combined,2*N,N)
    A_actual = G_actual / maxConductance
    R = 1 / G_actual[:N,:] 
    R2 = 1 / G_actual[N:,:]

    return A_actual, R, R2