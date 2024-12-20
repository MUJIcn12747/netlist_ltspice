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

from parameters import NUM_MATRIX, INPUT_PATH, NETLIST_PATH, OUTPUT_PATH, LTSPICE_EXE
from parameters import OPA,CIRCUIT,NEG_WEIGHT

from parameters import InterConnection_Resistor,Row_InterConnection_Resistor,Column_InterConnection_Resistor
from simulate import Get_Results

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

if __name__=='__main__':
    while(True):
        lines = ["Please choose a specific circuit for computing:", "0--mvm", "1--inv", "2--pinv"]
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

                    mvm_result, N, A, V, num_V = Get_Results(INPUT_FILE, NETLIST_DIR_MVM, CIRCUIT=0)
                    mvm_folder = os.path.join(OUTPUT_PATH, 'mvm')
                    os.makedirs(mvm_folder, exist_ok=True)
                    OUTPUT_FILE = os.path.join(mvm_folder, f"{i}.txt")
                    MVM_result(mvm_result, num_V, OUTPUT_FILE)

                    RESULT_VERIFY_DIR = os.path.join(mvm_folder, f"cmp{i}")
                    os.makedirs(RESULT_VERIFY_DIR, exist_ok=True)

                    for j in range(num_V):
                        mvm_ideal = np.dot(A, V[j])
                        mvm_test = mvm_result * mvm_ideal[0] / mvm_result[j, 0]
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

                    V_out, N, A, I, num_I = Get_Results(INPUT_FILE, NETLIST_DIR_INV, CIRCUIT=1)

                    inv_folder = os.path.join(OUTPUT_PATH, 'inv')
                    os.makedirs(inv_folder, exist_ok=True)
                    OUTPUT_FILE = os.path.join(inv_folder, f"{i}.txt")
                    INV_result(V_out, num_I, OUTPUT_FILE)                # result of inv

                    # I = I / np.max(I)
                    # print(I)                    # input current vector
                    RESULT_VERIFY_DIR = os.path.join(inv_folder, f"cmp{i}")
                    os.makedirs(RESULT_VERIFY_DIR, exist_ok=True)

                    for j in range(num_I):
                        I_test = np.dot(A, V_out[j])
                        I_test = I_test * I[j, 0] / I_test[0]
                        # I_test = I_test / I_test[np.argmax(np.abs(I_test))]
                        # print(I_test)
                        RESULT_VERIFY_FILE = os.path.join(RESULT_VERIFY_DIR, f"{j+1}.txt")
                        INV_result_verify(I_test, I[j], RESULT_VERIFY_FILE)
                E=time.time()
                print(E-S)

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
                        # I_test = np.dot(A, V_out[j])
                        # I_test = I_test * I[j, 0] / I_test[0]
                        RESULT_VERIFY_FILE = os.path.join(RESULT_VERIFY_DIR, f"{j+1}.txt")
                        PINV_result_verify(V_out[j], pinv_ideal, RESULT_VERIFY_FILE)
                E=time.time()
                print(E-S)

            case _:
                break        