import numpy as np
import time

from NetlistBuilder import Read_Param_inv
from NetlistBuilder import Read_Param_mvm
from NetlistBuilder import Read_Param_pinv

import subprocess
import os
import time
import matplotlib.pyplot as plt
import PyLTSpice 

from parameters import NUM_MATRIX, INPUT_PATH, NETLIST_PATH, OUTPUT_PATH, maxConductance, alpha_mvm, alpha_inv
from parameters import OPA,CIRCUIT,NEG_WEIGHT

from parameters import InterConnection_Resistor,Row_InterConnection_Resistor,Column_InterConnection_Resistor
from simulate import Get_Results
from positive_eig_check import check_positive_real_eigenvalues
from NoiseModel_Evaluation import Evaluation

def MVM_result(mvm_result, num_V, write_path):
    with open(write_path, "w") as file:
        for i in range(num_V):
            # Get the i-th row of V_out
            row = mvm_result[i]
            # Write the elements of the row to the file, separated by spaces
            file.write(" ".join([f"{value:.6f}" for value in row]) + "\n")

def MVM_result_verify(mvm_test, mvm_ideal, write_path):
    with open(write_path, 'w') as file:
        file.write('ideal      test\n')

        for i, j in zip(mvm_ideal, mvm_test):
            # 格式化数据，限制总长度为 10（包含小数部分和可能的负号）
            i_str = f"{round(i, 6):.6f}"[:10]  # 最多保留6位小数，截断到10字符
            j_str = f"{round(j, 6):.6f}"[:10]  # 同上
            file.write(f"{i_str.ljust(10)} {j_str.ljust(10)}\n")

def INV_result(V_out, num_V, write_path):
    with open(write_path, "w") as file:
        for i in range(num_V):
            # Get the i-th row of V_out
            row = V_out[i]
            # Write the elements of the row to the file, separated by spaces
            file.write(" ".join([f"{value:.6f}" for value in row]) + "\n")

def INV_stability_check(eigenvalues, positive_flag, condition_number, matrix_check_file):
    with open(matrix_check_file, "w") as file:
        file.write("Eigenvalues of the actual matrix M = UA:\n")
        for value in eigenvalues:
            file.write(f"{value}\n")
        if positive_flag:
            file.write("The real parts of all eigenvalues are positive\n")
        else:
            file.write("Not all eigenvalues have positive real part\n")
        file.write(f"Condition numbers of the actual matrix A: {condition_number}\n")

def INV_result_verify(I_test, I_ideal, write_path):
    with open(write_path, 'w') as file:
        file.write('Iideal     Itest\n')

        for i, j in zip(I_ideal, I_test):
            i_str = f"{round(i, 6):.6f}"[:10]  # 最多保留6位小数，截断到10字符
            j_str = f"{round(j, 6):.6f}"[:10]  # 同上
            file.write(f"{i_str.ljust(10)} {j_str.ljust(10)}\n")     

def PINV_result(V_out, num_V, write_path):
    with open(write_path, "w") as file:
        for i in range(num_V):
            # Get the i-th row of V_out
            row = V_out[i]
            # Write the elements of the row to the file, separated by spaces
            file.write(" ".join([f"{value:.6f}" for value in row]) + "\n")

def PINV_result_verify(V_test, V_ideal, write_path):
    with open(write_path, 'w') as file:
        file.write('Videal     Vtest\n')

        for i, j in zip(V_ideal, V_test):
            i_str = f"{round(i, 6):.6f}"[:10]  # 最多保留6位小数，截断到10字符
            j_str = f"{round(j, 6):.6f}"[:10]  # 同上
            file.write(f"{i_str.ljust(10)} {j_str.ljust(10)}\n")

def EIG_result(V_out, num_eig, write_path, eig_val):
    with open(write_path, "w") as file:
        file.write(f"Corresponding eigenvalue: {eig_val}\n")
        for i in range(num_eig):
            # Get the i-th row of V_out
            row = V_out[i]
            # Write the elements of the row to the file, separated by spaces
            file.write(" ".join([f"{value:.6f}" for value in row]) + "\n")

def EIG_result_verify(x_test, x_ideal, write_path, eig_val):
    with open(write_path, 'w') as file:
        file.write('ideal      test\n')

        for i, j in zip(x_ideal, x_test):
            i_str = f"{round(i, 6):.6f}"[:10]  # 最多保留6位小数，截断到10字符
            j_str = f"{round(j, 6):.6f}"[:10]  # 同上
            file.write(f"{i_str.ljust(10)} {j_str.ljust(10)}\n")

if __name__=='__main__':
    while(True):
        lines = ["Please choose a specific circuit for computing:", "0--mvm", "1--inv", "2--pinv", "3--eig"]
        text = "\n".join(lines)
        print(text)
        cir=int(input())
        match cir:
            case 0:
                '''mvm circuit test'''
                print('mvm_circuit_test')
                S=time.time()
                for i in range(1, NUM_MATRIX + 1):
                    INPUT_FILE = os.path.join(INPUT_PATH, 'mvm', f"{i}.txt") 
                    NETLIST_DIR_MVM = os.path.join(NETLIST_PATH, 'mvm',f"sp{i}")
                    os.makedirs(NETLIST_DIR_MVM, exist_ok=True)

                    mvm_result, N, M, A, V, num_V = Get_Results(INPUT_FILE, NETLIST_DIR_MVM, CIRCUIT=0)
                    mvm_folder = os.path.join(OUTPUT_PATH, 'mvm')
                    os.makedirs(mvm_folder, exist_ok=True)
                    OUTPUT_FILE = os.path.join(mvm_folder, f"{i}.txt")
                    MVM_result(mvm_result, num_V, OUTPUT_FILE)

                    RESULT_VERIFY_DIR = os.path.join(mvm_folder, f"cmp{i}")
                    os.makedirs(RESULT_VERIFY_DIR, exist_ok=True)

                    mvm_test = np.zeros_like(mvm_result)
                    for j in range(num_V):
                        mvm_ideal = np.dot(A, V[j])
                        mvm_test[j] = mvm_result[j] * np.max(A) * np.max(V[j]) / (alpha_mvm * maxConductance)
                        RESULT_VERIFY_FILE = os.path.join(RESULT_VERIFY_DIR, f"{j+1}.txt")
                        MVM_result_verify(mvm_test[j], mvm_ideal, RESULT_VERIFY_FILE)
                E=time.time()
                print(E-S)

            case 1:
                '''inv circuit test'''
                print('inv_circuit_test')
                S=time.time()
                for i in range(1, NUM_MATRIX + 1):
                    INPUT_FILE = os.path.join(INPUT_PATH, 'inv', f"{i}.txt")
                    NETLIST_DIR_INV = os.path.join(NETLIST_PATH, 'inv',f"sp{i}")
                    os.makedirs(NETLIST_DIR_INV, exist_ok=True)

                    V_out, N, A, I, num_I, A_actual = Get_Results(INPUT_FILE, NETLIST_DIR_INV, CIRCUIT=1)

                    eigenvalues, positive_flag = check_positive_real_eigenvalues(A_actual)
                    condition_number = np.linalg.cond(A_actual)
                    if not positive_flag:
                        print(f"Negative or non-real eigenvalue encountered at matrix {i}. Exiting simulation{i}.")
                        inv_folder = os.path.join(OUTPUT_PATH, 'inv')
                        os.makedirs(inv_folder, exist_ok=True)
                        MATRIX_CHECK_FILE = os.path.join(inv_folder, f"matrix_check{i}.txt")
                        INV_stability_check(eigenvalues, positive_flag, condition_number, MATRIX_CHECK_FILE)
                        continue

                    inv_folder = os.path.join(OUTPUT_PATH, 'inv')
                    os.makedirs(inv_folder, exist_ok=True)
                    OUTPUT_FILE = os.path.join(inv_folder, f"{i}.txt")
                    MATRIX_CHECK_FILE = os.path.join(inv_folder, f"matrix_check{i}.txt")
                    INV_stability_check(eigenvalues, positive_flag, condition_number, MATRIX_CHECK_FILE)
                    INV_result(V_out, num_I, OUTPUT_FILE)                                   # result of inv

                    RESULT_VERIFY_DIR = os.path.join(inv_folder, f"cmp{i}")
                    os.makedirs(RESULT_VERIFY_DIR, exist_ok=True)

                    x_out = np.zeros_like(V_out)
                    for j in range(num_I):
                        x_out[j] = V_out[j] * np.max(I[j]) / (alpha_inv * np.max(A))
                        I_test = np.dot(A, x_out[j])
                        # I_test = I_test * I[j, 0] / I_test[0]
                        RESULT_VERIFY_FILE = os.path.join(RESULT_VERIFY_DIR, f"{j+1}.txt")
                        INV_result_verify(I_test, I[j], RESULT_VERIFY_FILE)

                    # INV_result(x_out, num_I, OUTPUT_FILE)                                   # result of inv
                E=time.time()
                print(E-S)
                Evaluation()

            case 2:
                '''pinv circuit test'''
                print('pinv_circuit_test')
                S=time.time()
                for i in range(1, NUM_MATRIX + 1):
                    INPUT_FILE = os.path.join(INPUT_PATH, 'pinv', f"{i}.txt")
                    NETLIST_DIR_PINV = os.path.join(NETLIST_PATH, 'pinv',f"sp{i}")
                    os.makedirs(NETLIST_DIR_PINV, exist_ok=True)

                    V_out, N, M, A, I, num_I = Get_Results(INPUT_FILE, NETLIST_DIR_PINV, CIRCUIT=2)

                    pinv_folder = os.path.join(OUTPUT_PATH, 'pinv')
                    os.makedirs(pinv_folder, exist_ok=True)
                    OUTPUT_FILE = os.path.join(pinv_folder, f"{i}.txt")
                    PINV_result(V_out, num_I, OUTPUT_FILE)                # result of inv

                    RESULT_VERIFY_DIR = os.path.join(pinv_folder, f"cmp{i}")
                    os.makedirs(RESULT_VERIFY_DIR, exist_ok=True)

                    for j in range(num_I):
                        pinv_ideal=np.dot(A.T, A)
                        pinv_ideal=np.linalg.inv(pinv_ideal)
                        pinv_ideal=np.dot(pinv_ideal, A.T)
                        pinv_ideal=np.dot(pinv_ideal, I[j])
                        V_out[j] = V_out[j] * pinv_ideal[0] / V_out[j, 0]
                        RESULT_VERIFY_FILE = os.path.join(RESULT_VERIFY_DIR, f"{j+1}.txt")
                        PINV_result_verify(V_out[j], pinv_ideal, RESULT_VERIFY_FILE)
                E=time.time()
                print(E-S)

            case 3:
                '''eig circuit test'''
                print('eig_circuit_test')
                S=time.time()
                for i in range(1, NUM_MATRIX + 1):
                    INPUT_FILE = os.path.join(INPUT_PATH, 'eig', f"{i}.txt")
                    NETLIST_DIR_EIG = os.path.join(NETLIST_PATH, 'eig',f"sp{i}")
                    os.makedirs(NETLIST_DIR_EIG, exist_ok=True)

                    V_out, N, A, eig_lambda, num_eig, A_actual = Get_Results(INPUT_FILE, NETLIST_DIR_EIG, CIRCUIT=3)

                    # eigenvalues, positive_flag = check_positive_real_eigenvalues(A_actual)
                    condition_number = np.linalg.cond(A_actual)
                    # if not positive_flag:
                    #     print(f"Negative or non-real eigenvalue encountered at matrix {i}. Exiting simulation{i}.")
                    #     inv_folder = os.path.join(OUTPUT_PATH, 'inv')
                    #     os.makedirs(inv_folder, exist_ok=True)
                    #     MATRIX_CHECK_FILE = os.path.join(inv_folder, f"matrix_check{i}.txt")
                    #     INV_stability_check(eigenvalues, positive_flag, condition_number, MATRIX_CHECK_FILE)
                    #     continue

                    eig_folder = os.path.join(OUTPUT_PATH, 'eig')
                    os.makedirs(eig_folder, exist_ok=True)
                    OUTPUT_FILE = os.path.join(eig_folder, f"{i}.txt")
                    # MATRIX_CHECK_FILE = os.path.join(eig_folder, f"matrix_check{i}.txt")
                    # INV_stability_check(eigenvalues, positive_flag, condition_number, MATRIX_CHECK_FILE)
                    EIG_result(V_out, num_eig, OUTPUT_FILE, eig_lambda)                                   # result of eig

                    RESULT_VERIFY_DIR = os.path.join(eig_folder, f"cmp{i}")
                    os.makedirs(RESULT_VERIFY_DIR, exist_ok=True)

                    x_out = np.zeros_like(V_out)
                    eig_vals, eig_vecs = np.linalg.eig(A)
                    # for eig_value in eig_vals:
                    #     idx = np.where(np.isclose(eig_vals, eig_value))[0]
                    #     if len(idx) > 0:
                    #         EIG_result_verify(V_out[j], eig_vecs[:, idx[0]], RESULT_VERIFY_FILE)
                    for j in range(num_eig):
                        # V_out[j] = V_out[j] * eig_vecs[0, j] / V_out[j, 0]
                        V_out[j] = V_out[j] / V_out[j][np.argmax(np.abs(V_out[j]))]
                        eig_vecs[:, j] = eig_vecs[:, j] / eig_vecs[np.argmax(np.abs(eig_vecs[:, j])) , j]
                        RESULT_VERIFY_FILE = os.path.join(RESULT_VERIFY_DIR, f"{j+1}.txt")
                        EIG_result_verify(V_out[j], eig_vecs[:, j], RESULT_VERIFY_FILE, eig_vals[j])

                E=time.time()
                print(E-S)
            
            case _:
                break        