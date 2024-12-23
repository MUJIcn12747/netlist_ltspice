import numpy as np
import time
import subprocess
import os
import time
import matplotlib.pyplot as plt
import PyLTSpice 
import parameters as param
from OPAS import opa_
from Circuit import Circuit_
from parameters import maxConductance, minConductance, AM_or_QM, error_range_AM, num_Bit, sigma_QW, unit_Current, unit_Voltage, alpha_inv
from Mapping import Array_RealDevice_Update, InputVector_to_InputVoltage
'''输入文件:inputFile\i.txt
   输入格式:第一行矩阵规模N
            之后N*N权重电导
            之后任意个1*N电流向量'''
          

def Read_Param_inv(file_path):
    try:
        with open(file_path, 'r') as file:
            tmp = file.readline().strip()
            N=int(tmp)

            if N <= 0:
                raise ValueError("Array Size Error")
            data = []

            for i in range(N):
                line = file.readline().strip()
                numbers = list(map(float, line.split()))

                if len(numbers) != N:
                    raise ValueError("Array Number Error")
                data.append(numbers)
            A=np.array(data)

            data = []

            for line in file:
                line = line.strip()  # Remove any leading/trailing whitespace
                if line:  # Ignore empty lines
                    numbers = list(map(float, line.split()))  # Convert string to float

                    if len(numbers) != N:
                        raise ValueError("Array Number Error")
                    data.append(numbers)

            vector_b=np.array(data)
            num_b = vector_b.shape[0]
            return N, A ,vector_b, num_b
    
    except Exception as e:
        print(f"Read File Error: {e}")
        return None

def Read_Param_mvm(file_path):
    try:
        with open(file_path, 'r') as file:
            tmp = file.readline().strip()
            N=int(tmp)
            if N <= 0:
                raise ValueError("Array Size Error")
            data = []

            for i in range(N):
                line = file.readline().strip()
                numbers = list(map(float, line.split()))

                if len(numbers) != N:
                    raise ValueError("Array Number Error")
                data.append(numbers)
            A=np.array(data)

            data = []

            for line in file:
                line = line.strip()  # Remove any leading/trailing whitespace
                if line:  # Ignore empty lines
                    numbers = list(map(float, line.split()))  # Convert string to float

                    if len(numbers) != N:
                        raise ValueError("Array Number Error")
                    data.append(numbers)
            V=np.array(data)
            num_V = V.shape[0]
            return N, A, V, num_V
    
    except Exception as e:
        print(f"Read File Error: {e}")
        return None

def Read_Param_pinv(file_path):
    try:
        with open(file_path, 'r') as file:
            tmp = file.readline().strip()
            N=int(list(tmp.split())[0])
            M=int(list(tmp.split())[1])
            if (N <= 0) or (M <= 0):
                raise ValueError("Array Size Error")
            data = []

            for i in range(N):
                line = file.readline().strip()
                numbers = list(map(float, line.split()))

                if len(numbers) != M:
                    raise ValueError("Array Number Error")
                data.append(numbers)
            A=np.array(data)

            data = []

            for line in file:
                line = line.strip()  # Remove any leading/trailing whitespace
                if line:  # Ignore empty lines
                    numbers = list(map(float, line.split()))  # Convert string to float

                    if len(numbers) != N:
                        raise ValueError("Array Number Error")
                    data.append(numbers)

            I=np.array(data)
            num_I = I.shape[0]

            return N, M, A ,I, num_I
    
    except Exception as e:
        print(f"Read File Error: {e}")
        return None

def Build_inv(N, A, I, write_path, opa_id=0, NEG_WEIGHT=0):
    circuit=Circuit_()
    opa=opa_(opa_id)

    if (NEG_WEIGHT==0):
        G_actual = Array_RealDevice_Update(A,N,N)       # attach device model to conductance
        A_actual = G_actual / maxConductance
        R = 1 / G_actual                   # convert conductance to resistance
        V_in = InputVector_to_InputVoltage(I)
    else:                                   # real matrix with negative values
        A2=A.copy()
        for i in range(N):
            for j in range(N):
                if (A[i][j]>0):
                    A[i][j]=A[i][j]*2
                    A2[i][j]=A[i][j]/2
                else:
                    A[i][j]=-A[i][j]
                    A2[i][j]=A[i][j]*2
        A_combined=np.vstack((A,A2))
        '''
        g_min=np.min(A_combined)
        g_max=np.max(A_combined)
        if (g_max/g_min>10):
            A_combined=A_combined+g_max/9
        '''
        G_actual = Array_RealDevice_Update(A_combined,2*N,N)
        A_actual = G_actual / maxConductance
        R = 1 / G_actual[:N,:] 
        R2 = 1 / G_actual[N:,:]
        
        R_=100000
        V_in = InputVector_to_InputVoltage(I)

    for i in range(N):
        for j in range(N):
            r_num=N*i+j+1
            up_node=j+N+1
            down_node=i+1
            circuit.add_res(r_num,up_node,down_node,R[i][j])

    for i in range(N):                                                  # unit conductance
        r_num = '0' + str(i)
        up_node=i+2*N+1
        down_node=i+1
        circuit.add_res(r_num, up_node, down_node, 1/maxConductance)

    for i in range(N):
        node = i+2*N+1
        circuit.add_vdc(i+1, node, 0, V_in[i])

    voltage=opa.work_voltage()

    circuit.add_vdc(999,999,0,voltage)
    circuit.add_vdc(998,0,998,voltage)

    for i in range(N):
        node_in=i+1
        node_out=i+N+1
        circuit.add_opa(i+1,0,node_in,999,998,node_out,opa.name())

    if (NEG_WEIGHT==1):
        '''写入第二个阵列的电阻'''
        for i in range (N):
            for j in range(N):
                r_num=N*i+j+1+N*N
                up_node=j+3*N+1
                down_node=i+1
                circuit.add_res(r_num,up_node,down_node,R2[i][j])

        '''写入模拟反相器，电阻为1MΩ'''
        for i in range(N):#写入输入端电阻
            r_num=i+1+2*N*N
            up_node=i+N+1
            down_node=i+4*N+1
            circuit.add_res(r_num,up_node,down_node,R_)         
        for i in range(N):#写入输出端电阻
            r_num=N+i+1+2*N*N
            up_node=i+3*N+1
            down_node=i+4*N+1
            circuit.add_res(r_num,up_node,down_node,R_)
        for i in range(N):#写入运放    
            node_in=4*N+i+1
            node_out=i+3*N+1
            circuit.add_opa(i+1+N,0,node_in,999,998,node_out,opa.name())

    circuit.add_lib('LTC')
    circuit.add_lib('ADI')
    circuit.generate_netlist_file(write_path)
    circuit.clear()
    return A_actual


def Build_mvm(N, A, V, write_path, opa_id=0, NEG_WEIGHT=0):
    circuit=Circuit_()
    opa=opa_(opa_id)

    if (NEG_WEIGHT==0):                     # attach device model to conductance
        A_actual = Array_RealDevice_Update(A,N,N)
        A = 1 / A_actual                   # convert conductance to resistance
        V = V * unit_Voltage / np.max(V)
    else:                                   # real matrix with negative values
        Build_CCRS_mvm(N,A,V,write_path,opa_id)
        return
    
    R_=10000
    for i in range(N):
        for j in range(N):
            r_num=N*i+j+1
            up_node=j+N+1
            down_node=i+1
            circuit.add_res(r_num,up_node,down_node,A[i][j])

    for i in range(N):
        node=i+1+N
        circuit.add_vdc(i+1,node,0,V[i])

    voltage=opa.work_voltage()

    circuit.add_vdc(999,999,0,voltage)
    circuit.add_vdc(998,0,998,voltage)
    #结果转化为电压读出
    for i in range(N):#写入运放    
        node_in=i+1
        node_out=i+2*N+1
        circuit.add_opa(i+1,0,node_in,999,998,node_out,opa.name())

    for i in range(N):
        r_num=i+1+N*N
        up_node=i+1
        down_node=2*N+1+i
        circuit.add_res(r_num,up_node,down_node,R_)

    circuit.add_lib('LTC')
    circuit.add_lib('ADI')
    circuit.generate_netlist_file(write_path)
    circuit.clear()

def Build_CCRS_mvm(N, A, V, write_path, opa_id=0):
    circuit=Circuit_()

    A2=A.copy()
    '''计算补偿电阻'''
    g_row=np.zeros(N)
    g1_row=np.zeros(N)
    g_diff=np.zeros(N)
    g_min=np.min(np.abs(A))
    for i in range(N):
        for j in range(N):
            if (A[i][j]>0):
                A[i][j]=A[i][j]*2
                A2[i][j]=A[i][j]/2
            else:
                A2[i][j]=-A[i][j]*2
                A[i][j]=-A[i][j]
            g1_row[i]+=A2[i][j]
            g_row[i]+=A[i][j]

        g_diff[i]=g_row[i]-g1_row[i]
    
    for i in range(N):
        if (g_diff[i]>=0):
            g_row[i]=g_min
            g1_row[i]=g_min+g_diff[i]
        else:
            g_row[i]=(g_min-g_diff[i])
            g1_row[i]=g_min

    combined_conductance=np.vstack((A,A2,g_row,g1_row))
    g_min=np.min(combined_conductance)
    g_max=np.max(combined_conductance)
    #print(g_max,g_min)
    if (g_max/g_min>maxConductance/minConductance):
        combined_conductance=combined_conductance+g_max/9
    
    #print(combined_conductance)
    updated_combined_conductance=Array_RealDevice_Update(combined_conductance,N*2+2,N)
    A=1/updated_combined_conductance[:N,:]
    A2=1/updated_combined_conductance[N:2*N,:]
    g_row=1/updated_combined_conductance[2*N,:]
    g1_row=1/(updated_combined_conductance[2*N+1,:]+1e-4)
    V = V * unit_Voltage / np.max(V)
    opa=opa_(opa_id)

    for i in range(N):
        r_num=2*i+1+2*N*N
        up_node=0
        down_node=2*i+1
        circuit.add_res(r_num,up_node,down_node,g_row[i])

        r_num=2*i+2+2*N*N
        up_node=0
        down_node=2*i+2
        circuit.add_res(r_num,up_node,down_node,g1_row[i])
    for i in range(N):
        for j in range(N):
            r_num=N*i+j+1
            up_node=2*i+1
            down_node=j+1+3*N
            circuit.add_res(r_num,up_node,down_node,A[i][j])

            r_num=N*i+j+1+N*N
            up_node=2*i+2
            down_node=j+1+3*N
            circuit.add_res(r_num,up_node,down_node,A2[i][j])
    for i in range(N):
        node=i+1+3*N
        circuit.add_vdc(i+1,node,0,V[i])
    voltage=opa.work_voltage()
    circuit.add_vdc(999,999,0,voltage)
    circuit.add_vdc(998,0,998,voltage)
    #结果转化为电压读出
    for i in range(N):#写入运放    
        node_in_neg=2*i+1
        node_in_pos=2*i+2
        node_out=i+2*N+1
        circuit.add_opa(i+1,node_in_pos,node_in_neg,999,998,node_out,opa.name())
    R_=10000
    for i in range(N):
        r_num=i+1+2*N*N+2*N
        up_node=2*i+1
        down_node=2*N+1+i
        circuit.add_res(r_num,up_node,down_node,R_)
    circuit.add_lib('LTC')
    circuit.add_lib('ADI')
    circuit.generate_netlist_file(write_path)
    circuit.clear()

def Build_pinv(N, M, A, I, write_path, opa_id=0, NEG_WEIGHT=0):
    opa=opa_(opa_id)
    circuit=Circuit_()

    if (NEG_WEIGHT==0):                     # attach device model to conductance
        updated_A = Array_RealDevice_Update(A,N,M)
        A = 1 / updated_A                   # convert conductance to resistance
        I = I * unit_Current / np.max(I)
    else:                                   # real matrix with negative values
        A2=A.copy()                                   
        for i in range(N):
            for j in range(M):
                if (A[i][j]>0):
                    A[i][j]=A[i][j]*2
                    A2[i][j]=A[i][j]/2
                else:
                    A2[i][j]=-A[i][j]*2
                    A[i][j]=-A[i][j]
        A_combined = np.vstack((A,A2))
        g_min=np.min(A_combined)
        g_max=np.max(A_combined)
        #print(g_max,g_min)
        if (g_max/g_min>maxConductance/minConductance):
            A_combined=A_combined+g_max/9
        updated_A = Array_RealDevice_Update(A_combined,2*N,M)
        A = 1 / updated_A[:N,:] 
        A2 = 1 / updated_A[N:,:]            
        I = I * unit_Current / np.max(I)
    for i in range(N):
        for j in range(M):
            r_num=M*i+j+1
            up_node=i+1
            down_node=j+1+N
            circuit.add_res(r_num,up_node,down_node,A[i][j])

            r_num=M*i+j+1+N*M
            up_node=i+1+N+M
            down_node=j+1+2*N+M
            circuit.add_res(r_num,up_node,down_node,A[i][j])
    
    if (NEG_WEIGHT==1):
        for i in range(N):
            for j in range(M):
                r_num=M*i+j+1+2*N*M+N
                up_node=i+1+2*(N+M)
                down_node=j+1+N
                circuit.add_res(r_num,up_node,down_node,A2[i][j])

                r_num=M*i+j+1+3*N*M+N
                up_node=i+1+N+M
                down_node=j+1+2*N+M+2*(N+M)
                circuit.add_res(r_num,up_node,down_node,A2[i][j])
    for i in range(N):
        node=i+1
        circuit.add_idc(i+1,0,node,I[i])
    
    voltage=opa.work_voltage()
    circuit.add_vdc(999,999,0,voltage)
    circuit.add_vdc(998,0,998,voltage)

    for i in range(N):
        node_in_pos=0 if (NEG_WEIGHT==0) else i+1+2*(N+M)
        node_in_neg=i+1
        node_out=i+N+M+1
        circuit.add_opa(i+1,node_in_pos,node_in_neg,999,998,node_out,opa.name())

    R_=1000000
    for i in range(N):
        r_num=i+1+2*M*N
        up_node=i+1
        down_node=i+N+M+1
        circuit.add_res(r_num,up_node,down_node,R_)
    
    for i in range(M):
        node_in_pos=i+1+N+M+N
        node_in_neg=0 if (NEG_WEIGHT==0) else i+1+2*N+M+2*(N+M)
        node_out=i+1+N
        circuit.add_opa(i+1+N,node_in_pos,node_in_neg,999,998,node_out,opa.name())
    

    circuit.add_lib('LTC')
    circuit.add_lib('ADI')
    circuit.generate_netlist_file(write_path)
    circuit.clear()

if __name__=='__main__':
    Build_pinv('param_pinv.txt','pinv.cir',1)

