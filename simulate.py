import numpy as np
import time
from NetlistBuilder import Build_inv
from NetlistBuilder import Read_Param_inv
from NetlistBuilder import Build_mvm
from NetlistBuilder import Read_Param_mvm
from NetlistBuilder import Build_pinv
from NetlistBuilder import Read_Param_pinv
from rawread import read_voltage_inv,read_voltage_mvm,read_voltage_pinv
from positive_eig_check import check_positive_real_eigenvalues
from noise import Overall_output_noise
import subprocess
import os
import time
import matplotlib.pyplot as plt
import PyLTSpice 
from parameters import LTSPICE_EXE
from parameters import OPA,CIRCUIT,NEG_WEIGHT, maxConductance

'''
在parameters.py中修改电路参数
'''
def run_ltspice(NETLIST_PATH):
    """
    使用 LTspice 执行 Netlist 文件，并生成 RAW 文件。
    """
    cmd = [
        LTSPICE_EXE,
        '-Run',
        '-b',  
        NETLIST_PATH
    ]
    RAW_PATH=NETLIST_PATH.replace('.cir','.raw')
    try:
        S=time.time()
        subprocess.run(cmd, check=True)
        E=time.time()
        print('ltspice runtime:',E-S)
    except subprocess.CalledProcessError as e:
        print("simulation error:", e)
        return False
    return RAW_PATH

def Get_Results(INPUT_FILE, NETLIST_DIR, CIRCUIT):
    match CIRCUIT: 
        case 0: #mvm
            N, A, V, num_V=Read_Param_inv(INPUT_FILE)

            result_matrix = []

            for i in range(num_V):
                # Generate the file path for the netlist
                NETLIST_FILE = os.path.join(NETLIST_DIR, f"{i+1}.cir")
                Build_mvm(N, A.copy(), V[i].copy(), NETLIST_FILE, opa_id=OPA, NEG_WEIGHT=NEG_WEIGHT)
                RAW_FILE=run_ltspice(NETLIST_FILE)
                mvm_result=read_voltage_mvm(N, RAW_FILE)
                result_matrix.append(mvm_result)              # Append the current V vector to the list
            
            result_matrix = np.array(result_matrix)       # Convert the list of vectors into a NumPy array (num_I x N matrix)
            return result_matrix, N, A, V, num_V
        
        case 1: #inv
            N, A, I, num_I=Read_Param_inv(INPUT_FILE)

            V_matrix = []
            eigenvalues, positive_flag = check_positive_real_eigenvalues(A)

            if not positive_flag:
                return V_matrix, N, A, I, num_I

            for i in range(num_I):
                # Generate the file path for the netlist
                NETLIST_FILE = os.path.join(NETLIST_DIR, f"{i+1}.cir")
                A_actual = Build_inv(N, A.copy(), I[i].copy(), NETLIST_FILE, opa_id=OPA, NEG_WEIGHT=NEG_WEIGHT)
                RAW_FILE=run_ltspice(NETLIST_FILE)
                V = read_voltage_inv(N, RAW_FILE)
                V = Overall_output_noise(A_actual, V, N, maxConductance)                             # attach noise model to output vector
                V_matrix.append(V)                                      # Append the current V vector to the list
            
            V_matrix = np.array(V_matrix)                               # Convert the list of vectors into a NumPy array (num_I x N matrix)
            # print(V_matrix)
            return V_matrix, N, A, I, num_I

        case 2: #pinv
            N, M, A, I, num_I=Read_Param_pinv(INPUT_FILE)

            V_matrix = []

            for i in range(num_I):
                # Generate the file path for the netlist
                NETLIST_FILE = os.path.join(NETLIST_DIR, f"{i+1}.cir")
                Build_pinv(N, M, A.copy(), I[i].copy(), NETLIST_FILE, opa_id=OPA, NEG_WEIGHT=NEG_WEIGHT)
                RAW_FILE=run_ltspice(NETLIST_FILE)
                V=read_voltage_pinv(N, M, RAW_FILE)
                V_matrix.append(V)              # Append the current V vector to the list
            
            V_matrix = np.array(V_matrix)       # Convert the list of vectors into a NumPy array (num_I x N matrix)
            return V_matrix, N, M, A, I, num_I

        case _: return 0
    

