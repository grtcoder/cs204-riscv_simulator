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
#print("xx",len(machine_code))		
def fetch(pc):
	MC = []
	print("pc",pc)
	for i in range(32-len(machine_code[pc])):
		MC.append(int(0))
	for i in range(len(machine_code[pc])):
		MC.append(int(machine_code[pc][i]))
	print("fetched instruction at pc: ",pc)
	return MC
@dataclass
class PIP_REG:# buffer reg between deccode and execute 
	instruction=[] #mathpal dekhlena iska type and insert value here before doing IR.insert(0,temp)
	ins_type:str="None"
	pc:int=0
# 	RA:int=-1# these RA RB RZ are datapaths registers
# 	RB:int=-1
# 	RZ:int=-1
# 	RY:int=-1
	RA=[ -1 for i in range(32)]# these RA RB RZ are datapaths registers
	RB = [ -1 for i in range(32)]
	RZ = [ -1 for i in range(32)]
	RY = [ -1 for i in range(32)]
	immediate:int=-1
	ALU_OP:int=-1 
	b_SELECT:int=-1# used in alu, tells whether to take imm or register
	pc_select:int=-1 
	inc_select:int=-1
	#Y_SELECT:int#not useful as of now
	mem_read:int=-1
	mem_qty:int=-1
	mem_write:int=-1
	#RF_WRITE:int#not useful as of now
	address_a:int=-1#rs1
	address_b:int=-1#rs2
	address_c:int=-1#rd
	reg_id:int=-1#used only for write taken from read
	branchTaken:bool=False
	isFlushed:bool=False
	isBranchInstruction:bool=False
	isLoad:bool=False
	isStore:bool=False
	isALU:bool=False#lui and auipc true or false? right now i've taken it true!
	isJump:bool=False#jal and jalr
	isnull:bool=True#above boolean will help us easily identify and take action for hazards 
	stall:int=0
	state:int=1
	enable:int=0#not useful as of now
	enable2:int=1#not useful as of now
IR=[]
data_hazard=0
stalls_data_hazard=0
def run():
	#knob2=int(input("Enter value of knob2 "))
	clk=0
	global data_hazard
	a=PIP_REG()
	#IR=[] declared above
	for i in range(4):
		b=copy.deepcopy(a)
		IR.append(b)
	pc=0
	#IR[0].isnull=False
	#for i in range(4):
	#	print(IR[i].isnull)
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
	IR[0].isnull=False
	stall_temp=0
	loop_runner_for_last_instruction=0
	while(1 and loop_runner_for_last_instruction<4):	
		reg_id_temp=0
		rs1_temp=0
		w_val_temp=0
		if(IR[0].stall==0 and IR[0].isnull==False):
			IR[0].instruction=fetch(pc)
			IR[0].pc=copy.deepcopy(pc)
			#print(IR[1].isnull)
			IR[0].isnull=False
			#print(IR[1].isnull)
		
		if (IR[1].isFlushed == False and IR[1].stall==0 and IR[1].isnull==False):
			print("decode instruction")
			IR[1]=decode3(copy.deepcopy(IR[1]))
			print(" IR[1] ",IR[1].isFlushed,IR[1].stall,IR[1].isnull,IR[1].instruction,IR[1].ins_type)
		if (IR[2].isFlushed == False and IR[2].stall==0 and IR[2].isnull==False):
			print('execute instruction',binary(IR[2].RA),binary(IR[2].RB))
			IR[2] =   alu(copy.deepcopy(IR[2]))
			print("Value in RZ: ",IR[2].RZ)
			if(IR[2].branchTaken==True):# dont know the use of controlHazard function
				flush()
				pc=iag(IR[2].pc_select, IR[2].pc_enable, IR[2].inc_select, IR[2].immediate, IR[2].RA,IR[2].pc)
			#else: pc=pc+1	
				print('pc updated in IR[2] condition to ',pc )
		if IR[3].isFlushed == False and IR[3].stall==0 and IR[3].isnull==False:
			#print('MEM acces instruction')
			print("Mem access instruction",IR[3].ins_type,IR[3].mem_write,IR[3].mem_read)
			#reg_id_temp,rs1_temp,w_val_temp
			IR[3] = mem_read_write(copy.deepcopy(IR[3]))  ## function split from RW function
			#IR[3].RY=w_val_temp
			if(IR[3].isLoad==True) :
				if(IR[1].address_a ==   IR[3].address_c):
					IR[1].address_a=IR[3].RY
				if(IR[1].address_b ==   IR[3].address_c):
					IR[1].address_b=IR[3].RY
        ##### Check hazard
		ForwardDependency_MtoE()
		ForwardDependencyMtoM()
		ForwardDependency_EtoE()
		stall_temp=DataDependencyStall()
		temp=PIP_REG()
		IR.insert(0,copy.deepcopy(temp))
		IR[0].stall=stall_temp
		temp2=IR.pop()
		if(temp2.isnull==False):
			print('reg_write was done:value',binary(temp2.RY),"at id",temp2.reg_id)
			reg_write(copy.deepcopy(temp2))       ## functions split from RW function
		#print(stall_temp,len(machine_code),IR[2].branchTaken)
		if(stall_temp==0 and pc!=len(machine_code) and IR[3].branchTaken==False):
		   pc=pc+1
		#if(pc==0):
			#break
		#print('pc before if',pc)
		if(pc==len(machine_code) or pc==0):
			loop_runner_for_last_instruction+=1
			#print("holahup",loop_runner_for_last_instruction)
			IR[0].isnull=True
		else:
			IR[0].isnull=False
		clk+=1
# 		if(clk>10):
# 		 break
		print("clock" ,clk)
		print("*************************")
		print("*************************")
		#print(IR[2].stall)
        	 
			
			
			
			
			
#data hazard handling

#below three are just for data fwding
#below four are sufficient for data fwding logic need to write for stalling
def ForwardDependency_EtoE():
		global data_hazard
		#print(IR[1].address_a,IR[1].address_b,IR[2].address_c,IR[2].ins_type,IR[1].ins_type)
		if(IR[2].isnull==True or IR[1].isnull==True):
			return
		if (IR[2].address_c == 0):#EX-MEM's rd=0
			return
		if (IR[2].isJump == False and IR[2].isALU == False ):#EX-MM isnt alu and jal jalr
			return

		if (IR[1].address_a == IR[2].address_c and IR[1].address_b == IR[2].address_c): #rd of exmem = rs1 and rs2 of id_ex
			print("inside EtoE-1")
			data_hazard+=1
			IR[1].RA = IR[2].RZ
			IR[1].RB = IR[2].RZ
		if (IR[1].address_a == IR[2].address_c):#rd 0f exmem = rs1 of id_ex
			print("inside EtoE-2")
			data_hazard+=1
			IR[1].RA = IR[2].RZ
			return
		if (IR[1].address_b == IR[2].address_c):#rd of exmem = rs2 of id_ex
			print("inside EtoE- 3") 
			data_hazard+=1
			IR[1].RB = IR[2].RZ
			return
		return
def ForwardDependency_MtoE():
		global data_hazard
		if(IR[3].isnull==True or IR[1].isnull==True):
			return
		if (IR[3].address_c == 0):
			return
		if (IR[1].address_b == IR[3].address_c and IR[1].address_a == IR[3].address_c):
			print( "inside 1 MtoE" )
			data_hazard+=1
			IR[1].RA = IR[3].RY
			IR[1].RB = IR[3].RY
			return
		if (IR[1].address_a == IR[3].address_c):
			print( "inside 2 MtoE" )
			data_hazard+=1
			IR[1].RA = IR[3].RY
			return
		if (IR[1].address_b == IR[3].address_c):
			print( "inside 3 MtoE" )
			data_hazard+=1
			IR[1].RB = IR[3].RY
			return
		return
def ForwardDependencyMtoM():
		global data_hazard
		if(IR[2].isnull==True or IR[3].isnull==True):
			return
		if (IR[3].address_c == 0):
			return
		if (IR[3].isLoad == False):
			return

		if (IR[2].isStore == True):
		#Load-Store wali Dependency
			if (IR[2].address_b == IR[3].address_c):
				print ("MtoM") 
				data_hazard+=1
				IR[2].RB = IR[3].RY
				print("reg MEM_WB",IR[3].RY)
				return
			return
def DataDependencyStall():
	global stalls_data_hazard
	if(IR[2].isnull==True or IR[1].isnull==True):
			return 0
	if(IR[2].isLoad==True):
		if(IR[1].address_a ==    IR[2].address_c or    IR[1].address_b ==    IR[2].address_c):
			IR[1].stall=1
			stalls_data_hazard+=1
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

Stall_knob = map(int,input("Do you want Data Forwarding(0) or Data Stalling(1) to resolve dependencies?"))
run()
print(reg[3],reg[4])
