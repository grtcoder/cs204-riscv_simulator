from dataclasses import dataclass
from Phase_1_complete import *
from decode import *
from ALU import *
f = open('testing.asm', 'r+')
data = f.read().split('\n')
data1 = mc_gen(data).split('\n')
machine_code = []
for i in data1:
    z = toBinary(int(i, 0))
    machine_code.append(z)
def fetch(pc):
	MC = []
	for i in range(32-len(machine_code[pc])):
		MC.append(int(0))
	for i in range(len(machine_code[pc])):
		MC.append(int(machine_code[pc][i]))
	return MC
@dataclass
class PIP_REG:# buffer reg between deccode and  execute 
	pc:int
	RA:int
	RB:int
	RZ:int
	immediate:int
	ALU_OP:int 
    B_SELECT:int # used in alu, tells whether to take imm or register
    PC_SELECT:int 
    INC_SELECT:int 
    Y_SELECT:int
    MEM_READ:int
    MEM_WRITE:int
    RF_WRITE:int
	adrs_a:int
    adrs_b:int
    adrs_c:int
	return_add:int
	branchTaken:bool=False
	isBranchInstruction:bool=False
	isLoad:bool=False
	isStore:bool=False
	isALU:bool=False
	isJump:bool=False #jal and jalr
	isnull:False
    #above boolean will help us easily identify and take action for hazards
	stall:0
	state:1
	instruction:[]
    enable:int=0
	enable2:int=1

def run():
	knob2=int(input("Enter value of knob2 "))
	clk=0
	a=PIP_REG()
	IR=[]
	for i in range(5):
		IR.append(a)
	pc=0
	IR.append()
	while(1):
		clk+=1
		for i in range(min(clk,5)):
			if IR[i].state==1:
				IR[i].instruction=fetch(pc)
			elif IR[i].state==2:
				decode(IR[i].instruction)
			elif IR[i].state==3:
				alu(IR[i].instruction,IR[i].alu_op,IR[i].b_select,IR[i].ins_type)
			elif IR[i].state==4:
				####mem
			elif IR[i].state==5:
				####reg
			else:
				IR.pop()
				temp=PIP_REG()
				IR.append(temp)

			##### Check hazards