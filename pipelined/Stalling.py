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
# print(machine_code)
#print("xx",len(machine_code))		
def fetch(pc):
	MC = []
	print("pc",pc)
	for i in range(32-len(machine_code[pc])):
		MC.append(int(0))
	for i in range(len(machine_code[pc])):
		MC.append(int(machine_code[pc][i]))
	print("fetched instruction at pc: ",pc)
	print(MC)
	return MC
@dataclass
class PIP_REG:# buffer reg between deccode and execute 
	instruction=[] #mathpal dekhlena iska type and insert value here before doing IR.insert(0,temp)
	ins_type:str="None"
	pc:int=0
	RA:int=-1# these RA RB RZ are datapaths registers
	RB:int=-1
	RZ:int=-1
	RY:int=-1
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
just_fetched = 0
done = 0

#Data Stalling code starts here

def stall_run():
	clk=0
	global data_hazard
	a=PIP_REG()
	for i in range(4):
		b=copy.deepcopy(a)
		IR.append(b)
	pc=0
	stall_temp=0
	loop_runner_for_last_instruction=0
	IR[0].isnull = False
	while(1 and loop_runner_for_last_instruction<4):			
		# Stall_Program()

		print("r3: ",reg[3])

		if(IR[0].stall==0 and IR[0].isnull==False):
			IR[0].instruction=fetch(pc)
			# print("Fetched instruction: ",IR[0].ins_type)
			IR[0].pc=copy.deepcopy(pc)
			IR[0].isnull=False
		
		if (len(IR)>1 and IR[1].isFlushed == False and IR[1].isnull==False):
			IR[1]=decode3(copy.deepcopy(IR[1]))
			print("\t\t\t\t\t\tdecoding")
		
		if (len(IR)>2 and IR[2].isFlushed == False and IR[2].isnull==False):
			IR[2] = alu(copy.deepcopy(IR[2]))
			if(IR[2].branchTaken==True):
				flush()
				pc=iag(IR[2].pc_select, IR[2].pc_enable, IR[2].inc_select, IR[2].immediate, IR[2].RA,IR[2].pc)
		
		if (len(IR)>3 and IR[3].isFlushed == False and IR[3].isnull==False):
			IR[3] = mem_read_write(copy.deepcopy(IR[3]))  
		Stall_Program()
		
		for i in range(3):
			IR[i].stall = max(IR[i].stall-1,0)
		print("size: ",len(IR))
		for i in range(len(IR)):
			if(IR[0].stall == 0):
				break
			if (IR[i].stall == 0 and IR[i].isnull == False and IR[i].isFlushed == False):
				if(i == 0 or i == 4):
					break
				print("Adding buffer register ",i)
				temp = PIP_REG()
				IR.insert(i,temp)
				break
		temp2=IR.pop()
		if(temp2.isnull==False):				
			print('reg_write was done:value',(temp2.RY),"at id",temp2.reg_id)
			reg_write(copy.deepcopy(temp2))	
		# Stall_Program()
		# Stall_Program()
		stall_temp = IR[0].stall #if fetch is stalled, then stall other phases
		if(stall_temp == 0):
			temp=PIP_REG()
			IR.insert(0,copy.deepcopy(temp))
			IR[0].stall=0
		
		for i in range(len(IR)):
			print("Address ",i,IR[i].address_a,IR[i].address_b,IR[i].address_c,end = ' ')
			print("Stall time: ",IR[i].stall)
		if(stall_temp==0 and pc!=len(machine_code) and IR[3].branchTaken==False):
		   pc=pc+1

		if((pc==len(machine_code) or pc==0) and stall_temp == 0):
			loop_runner_for_last_instruction+=1
			IR[0].isnull=True
		
		else:
			IR[0].isnull=False
		
		clk+=1
		# if(clk>10):
		#  break
		print("clock" ,clk)
		print("*************************")
		print("*************************")

def Stall_Program():
	#call this function before executing current cycle to set the stall state for different IR's
	Stall_EtoE() #prev stores whether stall has been updated in this iteration or previous one.
	Stall_MtoE()
	Stall_MtoM()
	

def Stall_EtoE():
		global data_hazard
		#print(IR[1].address_a,IR[1].address_b,IR[2].address_c,IR[2].ins_type,IR[1].ins_type)
		if(IR[2].isnull==True or IR[1].isnull==True):
			return 
		if (IR[2].address_c == 0):#EX-MEM's rd=0
			return 
		if (IR[2].isJump == False and IR[2].isALU == False ):#EX-MM isnt alu and jal jalr
			return 
		if (len(IR)<3):
			return
		if (IR[1].address_a == IR[2].address_c and IR[1].address_b == IR[2].address_c): #rd of exmem = rs1 and rs2 of id_ex
			print("inside EtoE-1")
			data_hazard+=1
			IR[1].stall = 3 #stall this instruction
			IR[0].stall = 3
			return 
		if (IR[1].address_a == IR[2].address_c):#rd 0f exmem = rs1 of id_ex
			print("inside EtoE-2")
			data_hazard+=1
			IR[1].stall = 3
			IR[0].stall = 3
			return 
		if (IR[1].address_b == IR[2].address_c):#rd of exmem = rs2 of id_ex
			print("inside EtoE- 3") 
			data_hazard+=1
			IR[1].stall = 3
			IR[0].stall = 3
			return 
		return 

def Stall_MtoE():
		global data_hazard
		if (len(IR)<4):
			return
		if(IR[3].isnull==True or IR[1].isnull==True):
			return 
		if (IR[3].address_c == 0):
			return 
		if (IR[1].address_b == IR[3].address_c and IR[1].address_a == IR[3].address_c):
			print( "inside 1 MtoE" )
			data_hazard+=1
			IR[1].stall = max(IR[1].stall,2)
			IR[0].stall = max(IR[0].stall,2)
			return 
		if (IR[1].address_a == IR[3].address_c):
			print( "inside 2 MtoE" )
			data_hazard+=1
			IR[1].stall = max(IR[1].stall,2)
			IR[0].stall = max(IR[0].stall,2)
			return 
		if (IR[1].address_b == IR[3].address_c):
			print( "inside 3 MtoE" )
			data_hazard+=1
			IR[1].stall = max(IR[1].stall,2)
			IR[0].stall = max(IR[0].stall,2)
			return 
		return 

def Stall_MtoM():
		global data_hazard
		if(len(IR)<4):
			return
		if(IR[2].isnull==True or IR[3].isnull==True):
			return 
		if (IR[3].address_c == 0):
			return 

		if (IR[2].address_b == IR[3].address_c or IR[2].address_a == IR[3].address_c):
			print ("MtoM") 
			data_hazard+=1
			for i in range(3):
				IR[i].stall = max(IR[i].stall,2)
			print("reg MEM_WB",IR[3].RY)
			return 

#Data stalling code ends here
	
def controlHazard() :
	# jalr, beq, bne, bge, blt, jal
	if IR[2].isJump :                     # jal, jalr
		return 1
	if IR[2].isBranchInstruction :        # beg, bne, bgt, beq
		if IR[2].branchTaken :        
			return 1
	return 0

def flush() :
	IR[0]=PIP_REG()
	IR[1]=PIP_REG()
	IR[0].isFlushed = True
	IR[1].isFlushed = True
# Stall_knob = map(int,input("Data Forwarding(0) or Stalling(1) ?"))
stall_run()
print(reg[10])
