import random
import os
import numpy as np
from parameters import N_SIZE,ROW_PINV,COL_PINV,NUM_V,NUM_I,NUM_MATRIX,INPUT_PATH, CIRCUIT

def generate_numbers(N, row_pinv, col_pinv, num_V, num_I, num_Matrix, output_dir=INPUT_PATH):
    """
    Generates multiple files with the specified format:
    - First line: the number N.
    - Next N lines: each line contains N random real numbers between 1 and 4.
    - Last line: N random real numbers between 1 and 9.
    
    The files are named as 1.txt, 2.txt, ..., num_I.txt and saved in the specified directory.
    """
    # Ensure the directory exists
    os.makedirs(output_dir, exist_ok=True)

    for i in range(1, num_Matrix + 1):
        match CIRCUIT:
            case 0:
                mvm_folder = os.path.join(output_dir, 'mvm')
                os.makedirs(mvm_folder, exist_ok=True)
                output_file = os.path.join(mvm_folder, f"{i}.txt")

                with open(output_file, "w") as file:
                    # Write the first line: the number N
                    file.write(f"{N}\n")
            
                    # Write N lines of N random real numbers between 10 and 40
                    for _ in range(N):
                        random_numbers = [f"{random.uniform(10, 40):.2f}" for _ in range(N)]
                        file.write(" ".join(random_numbers) + "\n")
            
                    # Write the last line: N random real numbers between 1 and 9
                    for _ in range(num_V):
                        random_numbers = [f"{random.uniform(1, 9):.2f}" for _ in range(N)]
                        file.write(" ".join(random_numbers) + "\n")
            case 1:
                inv_folder = os.path.join(output_dir, 'inv')
                os.makedirs(inv_folder, exist_ok=True)
                output_file = os.path.join(inv_folder, f"{i}.txt")

                with open(output_file, "w") as file:
                    # Write the first line: the number N
                    file.write(f"{N}\n")
            
                    # Generate a random positive definite matrix
                    A = np.random.uniform(1, 4, size=(N, N))  # Generate random matrix
                    # positive_definite_matrix = A
                    positive_definite_matrix = np.dot(A.T, A)  # Ensure symmetry and positive definiteness

                    # Write the matrix to the file
                    for row in positive_definite_matrix:
                        file.write(" ".join(f"{value:.2f}" for value in row) + "\n")
            
                    # Write the last line: N random real numbers between 1 and 9
                    for _ in range(num_I):
                        random_numbers = [f"{random.uniform(1, 9):.2f}" for _ in range(N)]
                        file.write(" ".join(random_numbers) + "\n")
            case 2:
                pinv_folder = os.path.join(output_dir, 'pinv')
                os.makedirs(pinv_folder, exist_ok=True)
                output_file = os.path.join(pinv_folder, f"{i}.txt")

                with open(output_file, "w") as file:
                    # Write the first line:number of rows and columns
                    file.write(f"{row_pinv} {col_pinv}\n")
            
                    # Write N lines of N random real numbers between 10 and 40
                    for _ in range(row_pinv):
                        random_numbers = [f"{random.uniform(10, 40):.2f}" for _ in range(col_pinv)]
                        file.write(" ".join(random_numbers) + "\n")
            
                    # Write the last line: N random real numbers between 1 and 9
                    for _ in range(num_I):
                        random_numbers = [f"{random.uniform(1, 9):.2f}" for _ in range(row_pinv)]
                        file.write(" ".join(random_numbers) + "\n")
            case _:break 

# Example usage
N = N_SIZE                   # Replace with your desired value for N (size of matrix)
row_pinv = ROW_PINV
col_pinv = COL_PINV
num_V = NUM_V
num_I = NUM_I                   # number of input current vectors in inv
num_Matrix = NUM_MATRIX             # number of input conductance matrices
generate_numbers(N, row_pinv, col_pinv, num_V, num_I, num_Matrix)
