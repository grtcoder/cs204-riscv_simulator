from dataclasses import dataclass
from Phase_1_complete import *
from decode import *
from ALU import *
from Readwrite import *
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
class PIP_REG:# buffer reg between deccode and execute 
	pc:int=0
	RA:int# these RA RB RZ are datapaths registers
	RB:int
	RZ:int
	RY:int
	immediate:int
	ALU_OP:int 
	b_SELECT:int# used in alu, tells whether to take imm or register
	pc_select:int 
	inc_select:int 
	Y_SELECT:int
	mem_read:int
	mem_write:int
	RF_WRITE:int
	adress_a:int#rs1
	adress_b:int#rs2
	adress_c:int#rd
	return_add:int
	branchTaken:bool=False
	isFlushed:bool=False
	isBranchInstruction:bool=False
	isLoad:bool=False
	isStore:bool=False
	isALU:bool=False
	isJump:bool=False #jal and jalr
	isnull:False
    #above boolean will help us easily identify and take action for hazards
	stall:0
	state:1
	enable:int=0
	enable2:int=1
IR=[]
data_hazard=0
stalls_data_hazard=0
def run():
	knob2=int(input("Enter value of knob2 "))
	clk=0
	a=PIP_REG()
	#IR=[] declared above
	for i in range(4):
		IR.append(a)
	pc=0
	IR.append()
	while(1):
		clk+=1
		for i in range(min(clk,5)):
			if IR[i].state==1:
				IR[i].instruction=fetch(pc)
			elif IR[i].state==2 and IR[i].isFlushed == False:
				IR[i].type, IR[i].b_select, IR[i].ALU_op, IR[i].mem_read, IR[i].mem_write, IR[i].reg_write, IR[i].memqty, IR[i].pc_enable, IR[i].pc_select, IR[i].inc_select=decode(IR[i].instruction)
			elif IR[i].state==3 and IR[i].isFlushed == False:
				alu(IR[i].instruction,IR[i].alu_op,IR[i].b_select,IR[i].ins_type)
			elif IR[i].state==4 and IR[i].isFlushed == False:
				mem_read_write()## function split from RW function
			elif IR[i].state==5 and IR[i].isFlushed == False:
				reg_write()## functions split from RW function
			else:
				temp=PIP_REG()
				IR.insert(0,temp)
				IR.pop()

			##### Check hazard
			
			
			
			
			
#data hazard handling

#below threee are just for data fwding
#below four are sufficient for data fwding logic need to write for stalling
def ForwardDependency_EtoE(IR):
		if (IR[2].addressC == 0):#EX-MEM's rd=0
			return
		if (IR[2].isJump == False and IR[2].isALU == False ):#EX-MM isnt alu and jal jalr
			return

		if (IR[1].addressA == IR[2].addressC and IR[1].addressB == IR[2].addressC): #rd of exmem = rs1 and rs2 of id_ex
			print("inside EtoE-1")
			data_hazard=data_hazard+1
			IR[1].RA = IR[2].RZ
			IR[1].RB = IR[2].RZ
		if (IR[1].addressA == IR[2].addressC):#rd 0f exmem = rs1 of id_ex
			print("inside EtoE-2")
			data_hazard=data_hazard+1
			IR[1].RA = IR[2].RZ
			return
		if (IR[1].addressB == IR[2].addressC):#rd of exmem = rs2 of id_ex
			print("inside EtoE- 3") 
			data_hazard=data_hazard+1
			IR[1].RB = IR[2].RZ
			return
		return
def ForwardDependency_MtoE():
		if (IR[3].addressC == 0):
			return

		if (IR[1].addressB == IR[3].addressC and IR[1].addressA == IR[3].addressC):
			print( "inside 1 MtoE" )
			data_hazard=data_hazard+1
			IR[1].RA = IR[3].RY
			IR[1].RB = IR[3].RY
			return
		if (IR[1].addressA == IR[3].addressC):
			print( "inside 2 MtoE" )
			data_hazard=data_hazard+1
			IR[1].RA = IR[3].RY
			return
		if (IR[1].addressB == IR[3].addressC):
			print( "inside 3 MtoE" )
			data_hazard=data_hazard+1
			IR[1].RB = IR[3].RY
			return
		return
def ForwardDependencyMtoM():
		if (IR[3].addressC == 0):
			return
		if (IR[3].isLoad == False):
			return

		if (IR[2].isStore == True):
		#Load-Store wali Dependency
			if (IR[2].addressB == IR[3].addressC):
				print ("MtoM") 
				data_hazard=data_hazard+1
				IR[2].RB = IR[3].RY
				print("reg MEM_WB",IR[3].RY)
				return
			return

#this if for stalling it itself will increase cycle count
def forward_dependency_MtoEStall():
	
		if (   IR[3].addressC == 0):
			return  
		if (   IR[3].isLoad == False):
			return  
		if (   IR[2].isStore == True):
			return  
		if (   IR[1].addressA ==    IR[3].addressC and    IR[1].addressB ==    IR[3].addressC):
			print("forward_dependecy_MtoEStall 1")  
			data_hazard=data_hazard+1  
			stalls_data_hazard=stalls_data_hazard+1
			cycleCount=cycleCount+ 1
			IR[1].RA =    IR[3].RY  
			IR[1].RB =    IR[3].RY  
			return
		if (   IR[1].addressA ==    IR[3].addressC):
		   
			print("forward_dependecy_MtoEStall 2")  
			data_hazard+=1 
			stalls_data_hazard+=1  
			cycleCount+=1  
			IR[1].RA =    IR[3].RY  
			return  
		   
		if (   IR[1].addressB ==    IR[3].addressC):
		   
			print("forward_dependecy_MtoEStall 3")  
			data_hazard+=1 
			stalls_data_hazard+=1  
			cycleCount+=1
			IR[1].RB =    IR[3].RY  
			return  
		   
		return  
	
def controlHazard() :
	# jalr, beq, bne, bge, blt, jal
	if IR[2].isJump :                     # jal, jalr
		return 1
	if IR[2].isBranchInstruction :        # beg, bne, bgt, beq
		if IR[2].branchTaken :        
			return 1
	return 0

def flush() :
	IR[0].isFlushed = True
	IR[1].isFlushed = True
