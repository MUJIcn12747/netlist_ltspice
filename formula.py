import numpy as np
import time
import subprocess
import os
import time

def Calculate_diag_matrixU(matrix_A):
    row_sums = np.sum(matrix_A, axis=1)
    matrix_U = np.diag(1 / (1 + row_sums))
    return matrix_U

def Calculate_RT_n0(Boltzmann_k, Temperature, Circuit_Bandwidth, R0):
    n0 = np.sqrt(4 * Boltzmann_k * Temperature * Circuit_Bandwidth * R0)
    return n0