import numpy as np
import random
import time
import subprocess
import os
import time

def generate_positive_definite_matrix(N):
    # Generate a random matrix A
    A = np.random.uniform(1, 4, size=(N, N))
    
    A = np.dot(A.T, A)
    
    # Check if the matrix is positive definite by examining its eigenvalues
    # If not, increase the diagonal elements until all eigenvalues are positive
    while True:
        eigenvalues = np.linalg.eigvals(A)
        if np.all(eigenvalues > 0):  # All eigenvalues should be positive
            break
        # Increase the diagonal elements if the matrix is not positive definite
        for i in range(N):
            A[i, i] += random.uniform(1, 4)

    return A

# Generate a diagonal dominant matrix
def generate_diagonal_dominant_matrix(N):
    A = np.random.uniform(1, 4, size=(N, N))  # Generate a random matrix

    # Make it diagonally dominant
    for i in range(N):
        # Set the diagonal element to be larger than the sum of the non-diagonal elements in that row
        A[i, i] = np.sum(np.abs(A[i])) + random.uniform(1, 4)

    # Check if the matrix is positive definite by examining its eigenvalues
    # If not, increase the diagonal elements until all eigenvalues are positive
    while True:
        eigenvalues = np.linalg.eigvals(A)
        if np.all(eigenvalues > 0):  # All eigenvalues should be positive
            break
        # Increase the diagonal elements if the matrix is not positive definite
        for i in range(N):
            A[i, i] += random.uniform(1, 4)

    return A

def Calculate_diag_matrixU(matrix_A):
    row_sums = np.sum(matrix_A, axis=1)
    matrix_U = np.diag(1 / (1 + row_sums))
    return matrix_U

def Calculate_RT_n0(Boltzmann_k, Temperature, Circuit_Bandwidth, R0):
    n0 = np.sqrt(4 * Boltzmann_k * Temperature * Circuit_Bandwidth * R0)
    return n0