import numpy as np
import random
import time
import subprocess
import os
import time

def generate_positive_definite_matrix(N, min_value, max_value, scale=1.0):
    # Generate a random matrix A
    A = np.random.uniform(min_value, max_value, size=(N, N))
    
    A = np.dot(A.T, A)

    # To make the condition number smaller, we can adjust the diagonal elements to be more uniform
    # A diagonal matrix with similar values would reduce the condition number
    for i in range(N):
        A[i, i] += scale * random.uniform(min_value, max_value)
    
    # Check if the matrix is positive definite by examining its eigenvalues
    # If not, increase the diagonal elements until all eigenvalues are positive
    while True:
        eigenvalues = np.linalg.eigvals(A)
        if np.all(eigenvalues > 0):  # All eigenvalues should be positive
            break
        # Increase the diagonal elements if the matrix is not positive definite
        for i in range(N):
            A[i, i] += random.uniform(min_value, max_value)

    # To further improve the condition number, ensure the eigenvalues are closer together
    eigenvalues = np.linalg.eigvals(A)
    min_eigenvalue = np.min(eigenvalues)
    if min_eigenvalue < 1e-5:  # If smallest eigenvalue is very small, increase it
        A += np.eye(N) * abs(min_eigenvalue) * 10

    return A

# Generate a diagonal dominant matrix
def generate_diagonal_dominant_matrix(N, min_value, max_value):
    A = np.random.uniform(min_value, max_value, size=(N, N))  # Generate a random matrix

    # Make it diagonally dominant
    for i in range(N):
        # Set the diagonal element to be larger than the sum of the non-diagonal elements in that row
        A[i, i] = np.sum(np.abs(A[i])) + random.uniform(min_value, max_value)

    # Check if the matrix is positive definite by examining its eigenvalues
    # If not, increase the diagonal elements until all eigenvalues are positive
    while True:
        eigenvalues = np.linalg.eigvals(A)
        if np.all(eigenvalues > 0):  # All eigenvalues should be positive
            break
        # Increase the diagonal elements if the matrix is not positive definite
        for i in range(N):
            A[i, i] += random.uniform(min_value, max_value)

    return A

def Calculate_diag_matrixU(matrix_A):
    row_sums = np.sum(matrix_A, axis=1)
    matrix_U = np.diag(1 / (1 + row_sums))
    return matrix_U

def Calculate_Thermal_noise(Boltzmann_k, Temperature, Circuit_Bandwidth, R):
    noise = np.sqrt(4 * Boltzmann_k * Temperature * Circuit_Bandwidth * R)
    return noise

def Calculate_Relative_Error(ideal, test):
    # 计算ideal和test之间的2范数相对误差
    return np.linalg.norm(ideal - test) / np.linalg.norm(ideal)