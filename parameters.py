'''
circuit parameter
'''

N_SIZE = 5                      # Replace with your desired value for N (size of matrix)
ROW_PINV = 6                    # number of rows of pinv
COL_PINV = 4                    # number of columns of pinv
NUM_V = 5                       # number of input voltage vectors in mvm
NUM_I = 5                       # number of input current vectors in inv or pinv
NUM_MATRIX = 5                  # number of input conductance matrices
INPUT_PATH = r"inputFile"
NETLIST_PATH = r"NetlistFile"
OUTPUT_PATH = r"outputFile"
LTSPICE_EXE = r"E:\LTSpice\LTspice.exe"     # path of LTspice

OPA=1
'''
    0  LT1001
    1  AD823
    2  LT1632 (cmos)
    3  AD8606 (cmos)
'''

CIRCUIT=1
'''
0  mvm
1  inv
2  pinv
3  CC-RS mvm
'''

NEG_WEIGHT=0
'''
0  false
1  true
'''

'''
Cell model
'''
maxConductance = 200 * 1e-6		    # Maximum cell conductance (S)
minConductance = 20 * 1e-6	        # Minimum cell conductance (S)
AM_or_QM = True
error_range_AM = 0 * 1e-6
num_Bit = 10
sigma_QW = 1 * 1e-6
unit_Current = 200 * 1e-6                   # Maximum input current (A)
unit_Voltage = 0.2                          # Maximum input voltage (V)
alpha_inv = 0.01                            # Scaling factor for input of inv

InterConnection_Resistor=0   
Row_InterConnection_Resistor=0 
Column_InterConnection_Resistor=0

'''
Noise model
'''
Boltzmann_k = 1.38e-23
Temperature = 300               # Temperature in Kelvin (example value)
Circuit_Bandwidth = 1e6         # Bandwidth in Hz (example value)
sigma_FC = 1e-10
sigma_OA = 1e-10