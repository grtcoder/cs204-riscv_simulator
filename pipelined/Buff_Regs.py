from dataclasses import dataclass
from Phase_1_complete import *
from decode_phase3 import decode3
from ALU_Phase3 import *
from Readwrite import *
from iag_dp import *
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
class PIP_REG:# buffer reg between deccode and execute 
	instruction:[] #mathpal dekhlena iska type and insert value here before doing IR.insert(0,temp)
	ins_type:str
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
	Y_SELECT:int#not useful as of now
	mem_read:int
	memqty:int
	mem_write:int
	RF_WRITE:int#not useful as of now
	address_a:int#rs1
	address_b:int#rs2
	address_c:int#rd
	return_add:int#not used as of now
	branchTaken:bool=False
	isFlushed:bool=False
	isBranchInstruction:bool=False
	isLoad:bool=False
	isStore:bool=False
	isALU:bool=False#lui and auipc true or false? right now i've taken it true!
	isJump:bool=False #jal and jalr
	isnull:False
    #above boolean will help us easily identify and take action for hazards
	stall:0
	state:1
	enable:int=0#not useful as of now
	enable2:int=1#not useful as of now
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
	#IR.append()
	#fetch
	#IR[0]->buff reg IF_ID
	#decode
	#IR[1]
	#exec
	#IR[2]
	#MEM
	#IR[3]
	#WB
	while(1):
		clk+=1
		reg_id_temp=0
		rs1_temp=0
		w_val_temp=0
		if(IR[0].stall==0):
			IR[0].instruction=fetch(pc)
			IR[0].pc=copy.deepcopy(pc)
		
		if IR[1].isFlushed == False and IR[1].stall==0:
			 IR[1]=decode3(IR[1].instruction)
		if IR[2].isFlushed == False and IR[2].stall==0:
			IR[2].RZ,IR[2].branchTaken   =   alu(IR[2].instruction,IR[2].alu_op,IR[2].b_select,IR[2].ins_type)
			if(IR[2].branchTaken==True):# dont know the use of controlHazard function
				flush()
				pc=iag(IR[2].pc_select, IR[2].pc_enable, IR[2].inc_select, IR[2].immediate, IR[2].RA,IR[2].pc)
			else: pc=pc+1
		if IR[3].isFlushed == False and IR[3].stall==0:
			reg_id_temp,rs1_temp,w_val_temp    =   mem_read_write(IR[3].instruction, IR[3].RZ,IR[3].ins_type,IR[3].mem_read,IR[3].mem_write,IR[3].mem_qty,IR[3].pc)  ## function split from RW function
			IR[3].RY=w_val_temp
			if(IR[3].isLoad==True) :
				if(IR[1].address_a ==    IR[3].address_c):
					IR[1].address_a=IR[3].RY
				if(IR[1].address_b ==    IR[3].address_c):
					IR[1].address_b=IR[3].RY
        ##### Check hazard
		if(clk>=4):
			ForwardDependency_MtoE()
			ForwardDependencyMtoM()
		if(clk>=3):
			ForwardDependency_EtoE()
			stall_temp=DataDependencyStall()
		temp=PIP_REG()
		IR.insert(0,temp)
		IR[0].stall=stall_temp
		temp2=IR.pop()
		reg_write( temp2.instruction, temp2.RZ,temp2.ins_type,temp2.mem_read,temp2.mem_write,temp2.mem_qty,temp2.pc,reg_id_temp,w_val_temp)       ## functions split from RW function
		if(stall_temp==0):
		   pc++	
			
			
			
			
			
			
#data hazard handling

#below three are just for data fwding
#below four are sufficient for data fwding logic need to write for stalling
def ForwardDependency_EtoE():
		if (IR[2].address_c == 0):#EX-MEM's rd=0
			return
		if (IR[2].isJump == False and IR[2].isALU == False ):#EX-MM isnt alu and jal jalr
			return

		if (IR[1].address_a == IR[2].address_c and IR[1].address_b == IR[2].address_c): #rd of exmem = rs1 and rs2 of id_ex
			print("inside EtoE-1")
			data_hazard=data_hazard+1
			IR[1].RA = IR[2].RZ
			IR[1].RB = IR[2].RZ
		if (IR[1].address_a == IR[2].address_c):#rd 0f exmem = rs1 of id_ex
			print("inside EtoE-2")
			data_hazard=data_hazard+1
			IR[1].RA = IR[2].RZ
			return
		if (IR[1].address_b == IR[2].address_c):#rd of exmem = rs2 of id_ex
			print("inside EtoE- 3") 
			data_hazard=data_hazard+1
			IR[1].RB = IR[2].RZ
			return
		return
def ForwardDependency_MtoE():
		if (IR[3].address_c == 0):
			return

		if (IR[1].address_b == IR[3].address_c and IR[1].address_a == IR[3].address_c):
			print( "inside 1 MtoE" )
			data_hazard=data_hazard+1
			IR[1].RA = IR[3].RY
			IR[1].RB = IR[3].RY
			return
		if (IR[1].address_a == IR[3].address_c):
			print( "inside 2 MtoE" )
			data_hazard=data_hazard+1
			IR[1].RA = IR[3].RY
			return
		if (IR[1].address_b == IR[3].address_c):
			print( "inside 3 MtoE" )
			data_hazard=data_hazard+1
			IR[1].RB = IR[3].RY
			return
		return
def ForwardDependencyMtoM():
		if (IR[3].address_c == 0):
			return
		if (IR[3].isLoad == False):
			return

		if (IR[2].isStore == True):
		#Load-Store wali Dependency
			if (IR[2].address_b == IR[3].address_c):
				print ("MtoM") 
				data_hazard=data_hazard+1
				IR[2].RB = IR[3].RY
				print("reg MEM_WB",IR[3].RY)
				return
			return
def DataDependencyStall():
	if(IR[2].isLoad==True):
		if(IR[1].address_a ==    IR[2].address_c or    IR[1].address_b ==    IR[2].address_c):
			IR[1].stall=1
			return 1
	return 0

# #this if for stalling it itself will increase cycle count
# def forward_dependency_MtoEStall():
	
# 		if (   IR[3].address_c == 0):
# 			return  
# 		if (   IR[3].isLoad  == False):
# 			return  
# 		if (   IR[2].isStore == True):
# 			return  
# 		if (   IR[1].address_a ==    IR[3].address_c and    IR[1].address_b ==    IR[3].address_c):
# 			print("forward_dependecy_MtoEStall 1")  
# 			data_hazard=data_hazard+1  
# 			stalls_data_hazard=stalls_data_hazard+1
# 			#cycleCount=cycleCount+ 1
# 			IR[1].RA =    IR[3].RY  
# 			IR[1].RB =    IR[3].RY  
# 			return
# 		if (   IR[1].address_a ==    IR[3].address_c):
		   
# 			print("forward_dependecy_MtoEStall 2")  
# 			data_hazard+=1 
# 			stalls_data_hazard+=1  
# 			#cycleCount+=1  
# 			IR[1].RA =    IR[3].RY  
# 			return  
		   
# 		if (   IR[1].address_b ==    IR[3].address_c):
		   
# 			print("forward_dependecy_MtoEStall 3")  
# 			data_hazard+=1 
# 			stalls_data_hazard+=1  
# 			#cycleCount+=1
# 			IR[1].RB =    IR[3].RY  
# 			return  
		   
# 		return  
	
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
