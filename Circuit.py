from cells import res_,opas_,idcs_,vdcs_, vPWL_
import numpy as np
from parameters import T_MIN, T_MAX

class Circuit_():
    res_list = []
    opa_list = []
    idc_list = []
    vdc_list = []
    vPWL_list = []
    lib_list = []

    def __init__(self):
        pass

    def add_res(self,id,node1,node2,value):
        res=res_(id,node1,node2,value)
        self.res_list.append(res)
    
    def add_opa(self,id,n1,n2,n3,n4,n5,name):
        opa=opas_(id,n1,n2,n3,n4,n5,name)
        self.opa_list.append(opa)

    def add_vdc(self,id,node_pos,node_neg,value):
        vdc=vdcs_(id,node_pos,node_neg,value)
        self.vdc_list.append(vdc)

    def add_idc(self,id,node_pos,node_neg,value):
        idc=idcs_(id,node_pos,node_neg,value)
        self.idc_list.append(idc)

    def add_vPWL(self, id, node_pos, node_neg):
        vPWL = vPWL_(id, node_pos, node_neg)
        self.vPWL_list.append(vPWL)

    def add_lib(self,lib_name):
        self.lib_list.append(lib_name)

    def generate_netlist_file(self,FILE_NAME):
        with open(FILE_NAME, 'w') as file:
            file.write('* ltspice_circuit_netlist\n')
            for res in self.res_list:
                file.write(res.netlist_format())
            for opas in self.opa_list:
                file.write(opas.netlist_format())
            for vdcs in self.vdc_list:
                file.write(vdcs.netlist_format())
            for idcs in self.idc_list:
                file.write(idcs.netlist_format())
            for vPWL in self.vPWL_list:
                file.write(vPWL.netlist_format())
            for libs in self.lib_list:
                file.write('.lib '+libs+'.lib\n')
            file.write(f'.tran {T_MIN} {T_MAX}\n')
            file.write('.backanno\n')
            file.write('.end\n')
        file.close()
    
    def clear(self):
        self.res_list.clear()
        self.opa_list.clear()
        self.idc_list.clear()
        self.vdc_list.clear()
        self.vPWL_list.clear()
        self.lib_list.clear()
