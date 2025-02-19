import numpy as np
import time
from NetlistBuilder import Build_inv
from NetlistBuilder import Read_Param_inv
from NetlistBuilder import Build_mvm
from NetlistBuilder import Read_Param_mvm
from NetlistBuilder import Build_pinv
from NetlistBuilder import Read_Param_pinv
from NetlistBuilder import Build_eig
from NetlistBuilder import Read_Param_eig
from NetlistBuilder import Build_inv_randNoise
from rawread import read_voltage_inv, read_voltage_mvm, read_voltage_pinv, read_voltage_eig
from positive_eig_check import check_positive_real_eigenvalues
from Mapping import InputVector_to_InputVoltage, Mapping_inv_pos, Mapping_inv_neg, Eigenvalue_to_Glambda, Mapping_eig_pos
from noise import Overall_output_noise
from RandomNoise_generator import gen_randNoise
import subprocess
import os
import time
import matplotlib.pyplot as plt
import PyLTSpice 
from parameters import LTSPICE_EXE
from parameters import OPA,CIRCUIT,NEG_WEIGHT, maxConductance, Add_Noise
from parameters import T_MIN, T_MAX

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
                result_matrix.append(mvm_result)                # Append the current V vector to the list
            
            result_matrix = np.array(result_matrix)             # Convert the list of vectors into a NumPy array (num_I x N matrix)
            return result_matrix, N, A, V, num_V
        
        case 1: #inv
            N, A, vector_b, num_I=Read_Param_inv(INPUT_FILE)

            V_out = []
            if (NEG_WEIGHT==0):
                A_actual, R, R2 = Mapping_inv_pos(N, A.copy())
            else:                                                       # real matrix with negative values
                A_actual, R, R2 = Mapping_inv_neg(N, A.copy())

            gen_randNoise(R, N, T_MIN, T_MIN, T_MAX, NETLIST_DIR)

            for i in range(num_I):
                # Generate the file path for the netlist
                NETLIST_FILE = os.path.join(NETLIST_DIR, f"{i+1}.cir")
                V_in = InputVector_to_InputVoltage(vector_b[i].copy())
                Build_inv(N, R, R2, V_in, NETLIST_FILE, opa_id=OPA, NEG_WEIGHT=NEG_WEIGHT)
                # Build_inv_randNoise(N, R, R2, V_in, NETLIST_FILE, opa_id=OPA, NEG_WEIGHT=NEG_WEIGHT)

                eigenvalues, positive_flag = check_positive_real_eigenvalues(A_actual)
                if not positive_flag:
                    return V_out, N, A, vector_b, num_I, A_actual
                
                RAW_FILE=run_ltspice(NETLIST_FILE)
                V = read_voltage_inv(N, RAW_FILE)
                if Add_Noise:
                    V = Overall_output_noise(A_actual, V, N, maxConductance)                             # attach noise model to output vector
                V_out.append(V)                                      # Append the current V vector to the list
            
            V_out = np.array(V_out)                               # Convert the list of vectors into a NumPy array (num_I x N matrix)
            return V_out, N, A, vector_b, num_I, A_actual

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

        case 3: #eig
            N, A, eig_lambda, num_eig = Read_Param_eig(INPUT_FILE)

            V_out = []
            if (NEG_WEIGHT==0):
                A_actual, R, R2 = Mapping_eig_pos(N, A.copy(), eig_lambda.copy())
            # else:                                                       # real matrix with negative values
            #     A_actual, R, R2 = Mapping_eig_neg(N, A.copy())

            # gen_randNoise(R, N, T_MIN, T_MIN, T_MAX, NETLIST_DIR)

            for i in range(num_eig):
                # Generate the file path for the netlist
                NETLIST_FILE = os.path.join(NETLIST_DIR, f"{i+1}.cir")
                G_lambda = Eigenvalue_to_Glambda(A.copy(), eig_lambda[i], eig_lambda.copy())
                Build_eig(N, R, R2, G_lambda, NETLIST_FILE, opa_id=OPA, NEG_WEIGHT=NEG_WEIGHT)
                # Build_inv_randNoise(N, R, R2, V_in, NETLIST_FILE, opa_id=OPA, NEG_WEIGHT=NEG_WEIGHT)

                # eigenvalues, positive_flag = check_positive_real_eigenvalues(A_actual)
                # if not positive_flag:
                #     return V_out, N, A, vector_b, num_I, A_actual
                
                RAW_FILE=run_ltspice(NETLIST_FILE)
                V = read_voltage_eig(N, RAW_FILE)
                # if Add_Noise:
                #     V = Overall_output_noise(A_actual, V, N, maxConductance)                             # attach noise model to output vector
                V_out.append(V)                                      # Append the current V vector to the list
            
            V_out = np.array(V_out)                               # Convert the list of vectors into a NumPy array (num_I x N matrix)
            return V_out, N, A, eig_lambda, num_eig, A_actual
        
        case _: return 0
    

