from PyLTSpice import RawRead
from matplotlib import pyplot as plt
import numpy as np
def read_voltage_inv(N,RAW_FILE_PATH):

    LTR = RawRead(RAW_FILE_PATH)
    V=[]
    for i in range(N):
        node_read=i+1+N
        V_="V(N" + str(node_read).zfill(3)+')'
        #print(V_)
        V_i = LTR.get_trace(V_)
        voltage_wave_i= V_i.get_wave(0)
        V.append(voltage_wave_i[0])
    return V

def read_voltage_mvm(N,RAW_FILE_PATH):

    LTR = RawRead(RAW_FILE_PATH)
    V=[]
    for i in range(N):
        node_read=i+1+2*N
        V_="V(N" + str(node_read).zfill(3)+')'
        #print(V_)
        V_i = LTR.get_trace(V_)
        voltage_wave_i= V_i.get_wave(0)
        V.append(voltage_wave_i[0])
    return V

def read_voltage_pinv(N,M,RAW_FILE_PATH):

    LTR = RawRead(RAW_FILE_PATH)
    V=[]
    for i in range(M):
        node_read=i+1+N
        V_="V(N" + str(node_read).zfill(3)+')'
        #print(V_)
        V_i = LTR.get_trace(V_)
        voltage_wave_i= V_i.get_wave(0)
        V.append(voltage_wave_i[0])
    return V
    
if __name__=='__main__':
    res=read_voltage_mvm(5,'mvm.raw')
    print(res)