import numpy as np
import time
import subprocess
import os
import time
from parameters import Boltzmann_k, Temperature, Circuit_Bandwidth, sigma_FC, sigma_OA
from formula import Calculate_Thermal_noise, Calculate_diag_matrixU

class Noise_():
    def __init__(
        self,
        A_actual
    ):
        self.A_actual = A_actual
        self.local_gen = np.random.default_rng()

    def Former_Circuit_noise(
        self,
        V_out,
        N
    ):
        noise_FC = np.zeros_like(V_out)
        for i in range(N):
            noise_FC[i] = self.local_gen.normal(0, sigma_FC) 
        A_actual_inv = np.linalg.inv(self.A_actual)
        V_out = V_out - A_actual_inv @ noise_FC
        return V_out

    def Resistance_Thermal_noise(
        self,
        V_out,
        N,
        unit_Conductance
    ):
        R0 = 1 / unit_Conductance
        n0 = Calculate_Thermal_noise(Boltzmann_k, Temperature, Circuit_Bandwidth, R0)

        noise_rt = np.zeros_like(V_out)
        unit_Conductance_rt = np.zeros_like(V_out)
        row_sums = np.sum(self.A_actual, axis=1)
        for i in range(N):
            noise_rt[i] = self.local_gen.normal(0, np.sqrt(row_sums[i]))
            unit_Conductance_rt[i] = self.local_gen.normal(0, 1)
        A_actual_inv = np.linalg.inv(self.A_actual)
        V_out = V_out + n0 * (A_actual_inv @ noise_rt + A_actual_inv @ unit_Conductance_rt)
        return V_out

    def OPA_Noise(
        self,
        V_out,
        N
    ):   
        U_actual = Calculate_diag_matrixU(self.A_actual)
        M_actual = U_actual * self.A_actual
        noise_OA = np.zeros_like(V_out)
        for i in range(N):
            noise_OA[i] = self.local_gen.normal(0, sigma_OA) 
        V_out = V_out + np.linalg.inv(M_actual) @ noise_OA
        return V_out
    
def Overall_output_noise(A_actual, V_out, N, unit_Conductance):
    noise_model = Noise_(A_actual)
    V_out = noise_model.Former_Circuit_noise(V_out, N)
    V_out = noise_model.Resistance_Thermal_noise(V_out, N, unit_Conductance)
    V_out = noise_model.OPA_Noise(V_out, N)
    return V_out