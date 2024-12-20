class opa_:
    id=2
    '''
    0  LT1001
    1  AD823
    2  LT1632 (cmos)
    3  AD8606 (cmos)
    '''
    def name(self):
        match self.id:
            case 0: return 'LT1001'
            case 1: return 'AD823'
            case 2: return 'LT1632' 
            case 3: return 'AD8606'
            case _: return 'LT1001'

    def work_voltage(self):
        match self.id:
            case 0: return 12
            case 1: return 5
            case 2: return 3
            case 3: return 3
            case _:return 12 
    def __init__(self,opa_id):
        self.id=opa_id
