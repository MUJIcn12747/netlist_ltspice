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
    return A_actual

def InputVector_to_InputVoltage(vector_b):
    Voltage = (-1) * vector_b * alpha_inv / np.max(vector_b)
    return Voltage