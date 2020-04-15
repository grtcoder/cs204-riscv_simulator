from decode import *
import copy
from Phase_1_complete import *
from ALU_Phase3 import *
#from get_immediate import *
from Readwrite import *
from iag_dp import *


# PC = 0
SIZE = 1 << 32
SIZE -= 1


def _2C(n):
    m = SIZE
    m = m ^ n
    return add(m)


f = open('testing.asm', 'r+')
data = f.read().split('\n')
data1 = mc_gen(data).split('\n')
# print(data1)
# print(data1)4


def run(machine_code, temp):
    # temp=copy.deepcopy(PC)
    MC = []
    for i in range(32-len(machine_code)):
        MC.append(int(0))
    for i in range(len(machine_code)):
        MC.append(int(machine_code[i]))
    #print('MC ',MC)
    type, b_select, ALU_op, mem_read, mem_write, reg_write, memqty, pc_enable, pc_select, inc_select = decode(MC)
    res = str(alu(MC, ALU_op, b_select, type))
    # print("aluval: {}".format(binary([int(c) for c in res])))
    if(type=="SB"):
        if(int(res)==int(0)):
            inc_select=0
    reg_id=RW(MC, res, type, mem_read, mem_write, memqty,temp)
    imm = get_immediate(MC, type)
    #print('returned by get_imm ',imm)
    #reg_id = binary(machine_code[20:25])
    #print(reg_id)
    # print(ALU_op)
    return iag(pc_select, pc_enable, inc_select, imm, reg[reg_id], temp)
    
def full_run(data1, PC):
    if(data1 != ['']):
        data2 = []
        for i in data1:
            z = toBinary(int(i, 0))
            data2.append(z)
        
        #for i in range(0, len(data2)): 
        #    data2[i] = int(data2[i]) 
        # print(data2)
        # print(len(data2))
        # print(len(data2))
        while PC < len(data2):
            # print(reg[1])
            temp = copy.deepcopy(PC)
            # print(PC, data2[temp])
            print("PC: {}".format(PC))
            PC = run(data2[temp], temp)
            print("x10: {}".format(binary(reg[10])))
            if(PC == 0):
                break
            i=0
            for _ in reg:
                #print(i,end=" ")
                #print(binary(_))
                i+=1
# print(data1)
full_run(data1, 0)
i=0