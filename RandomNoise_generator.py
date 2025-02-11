import numpy as np
import time
import subprocess
import os
import time
from parameters import maxConductance, Boltzmann_k, Temperature, Circuit_Bandwidth
from formula import Calculate_Thermal_noise

def gen_randNoise(R, N, begin_time, t_min, t_max, randNoise_path):
    
    simulation_time = np.arange(begin_time, t_max + t_min, t_min)
    local_gen = np.random.default_rng()
    noise_dir = randNoise_path
    
    # noise_dir = os.path.join(randNoise_path, 'NoiseFile')
    os.makedirs(noise_dir, exist_ok=True)

    sigma_thermal_noise = Calculate_Thermal_noise(Boltzmann_k, Temperature, Circuit_Bandwidth, R)
    for i in range(N):
        for j in range(N):
            vPWL_num = N*i+j+1
            noise_file = os.path.join(noise_dir, f"randNoise{vPWL_num}.txt")
            with open(noise_file, 'w') as file:
                for time in simulation_time:
                    random_value = local_gen.normal(0, sigma_thermal_noise[i][j])
                    file.write(f"{time} {random_value}\n")

    sigma_thermal_n0 = Calculate_Thermal_noise(Boltzmann_k, Temperature, Circuit_Bandwidth, 1/maxConductance)
    for i in range(N):
        vPWL_num = '0' + str(i)
        noise_file = os.path.join(noise_dir, f"randNoise{vPWL_num}.txt")
        with open(noise_file, 'w') as file:
            for time in simulation_time:
                random_value = local_gen.normal(0, sigma_thermal_n0)
                file.write(f"{time} {random_value}\n")
