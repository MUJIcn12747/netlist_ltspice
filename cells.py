class res_():
    value=0
    node1=0
    node2=0
    id=0
    def __init__(self,id,node1,node2,value):
        self.id=id
        self.value=value
        self.node1=node1
        self.node2=node2
    
    def netlist_format(self):
        node_name_1 = ("N" + str(self.node1).zfill(3)) if (self.node1!=0) else '0'
        node_name_2 = ("N" + str(self.node2).zfill(3)) if (self.node2!=0) else '0'
        format = f"R{self.id} {node_name_1} {node_name_2} {self.value}\n"
        return format

class opas_():
    node_pos=0
    node_neg=0
    node_vdd=0
    node_vss=0
    node_out=0
    id=0
    names=''
    def __init__(self,id,node_pos,node_neg,node_vdd,node_vss,node_out,names):
        self.id=id
        self.node_pos=node_pos
        self.node_neg=node_neg
        self.node_vdd=node_vdd
        self.node_vss=node_vss
        self.node_out=node_out
        self.names=names

    def netlist_format(self):
        node_name_pos = ("N" + str(self.node_pos).zfill(3)) if (self.node_pos!=0) else '0'
        node_name_neg = ("N" + str(self.node_neg).zfill(3)) if (self.node_neg!=0) else '0'
        node_name_vdd = ("N" + str(self.node_vdd).zfill(3)) if (self.node_vdd!=0) else '0'
        node_name_vss = ("N" + str(self.node_vss).zfill(3)) if (self.node_vss!=0) else '0'
        node_name_out = ("N" + str(self.node_out).zfill(3)) if (self.node_out!=0) else '0'
        row_format=f"XU{self.id} {node_name_pos} {node_name_neg} {node_name_vdd} {node_name_vss} {node_name_out} "+self.names+"\n"
        return row_format

class vdcs_():
    value=0 
    id=0
    node_pos=0
    node_neg=0

    def __init__(self,id,node_pos,node_neg,value):
        self.value=value
        self.id=id
        self.node_pos=node_pos
        self.node_neg=node_neg

    def netlist_format(self):
        node_name_pos = ("N" + str(self.node_pos).zfill(3)) if (self.node_pos!=0) else '0'
        node_name_neg = ("N" + str(self.node_neg).zfill(3)) if (self.node_neg!=0) else '0'
        format = f"V{self.id} {node_name_pos} {node_name_neg} {self.value} Rser=0\n"
        return format

class idcs_():
    value=0 
    id=0
    node_pos=0
    node_neg=0

    def __init__(self,id,node_pos,node_neg,value):
        self.value=value
        self.id=id
        self.node_pos=node_pos
        self.node_neg=node_neg
    
    def netlist_format(self):
        node_name_pos = ("N" + str(self.node_pos).zfill(3)) if (self.node_pos!=0) else '0'
        node_name_neg = ("N" + str(self.node_neg).zfill(3)) if (self.node_neg!=0) else '0'
        format = f"I{self.id} {node_name_pos} {node_name_neg} {self.value}\n"
        return format