from dataclasses import dataclass
from Phase_1_complete import *
from decode_phase3 import decode3
from ALU_Phase3 import *
from Readwrite import *
from iag_dp import *
from btb import *
f = open('pipelined/testing.asm', 'r+')
data = f.read().split('\n')
data1 = mc_gen(data).split('\n')

Regout=open('pipelined/Reg_File.rtf','r+')
pipout=open('pipelined/pip_regsout.rtf','r+')
debugf=open('pipelined/debugf.rtf','r+')
Knob5out=open('pipelined/Knob5.rtf','r+')
outfile=open('pipelined/output_all.rtf','r+')

machine_code = []
for i in data1:
    z = toBinary(int(i, 0))
    machine_code.append(z)
#print("xx",len(machine_code))		
def fetch(pc):
	MC = []
	print("pc",pc,debugf)
	for i in range(32-len(machine_code[pc])):
		MC.append(int(0))
	for i in range(len(machine_code[pc])):
		MC.append(int(machine_code[pc][i]))
	#print("fetched instruction at pc: ",pc,IR[2].isFlushed,IR[2].isnull,IR[2].stall,"hhhhhhhhhhhhhhhhhhhhhhhh",pc,file=debugf)
	return MC
@dataclass
class PIP_REG:# buffer reg between deccode and execute 
	instruction=[] # type and insert value here before doing IR.insert(0,temp)
	ins_type:str="None"
	pc:int=0
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
	target_loaded:bool=False
	enable:int=0#not useful as of now
	enable2:int=1#not useful as of now
IR=[]
data_hazard=0
ctrl_hazard=0
stalls_data_hazard=0
branch_miss_predict=0
def run():
	knob3= int(input("Enable(1)/disable(0) printing values in the register file at the end of each cycle:  "))
	knob4=int(input("Enable(1)/disable(0) printing information in the pipeline registers at the end of each cycle: "))
	knob5=int(input("Print information in the pipeline registers for instruction no(-1 to disable): "))
	clk=0
	global data_hazard
	global ctrl_hazard
	global stalls_data_hazard
	global branch_miss_predict
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
	total_executions=0
	total_ctrlinst=0
	total_dfinst=0
	total_aluinst=0
	IR[0].isnull=False
	stall_temp=0
	loop_runner_for_last_instruction=0
	hashmap = branch_target_buffer()
	while(loop_runner_for_last_instruction<4):	
		reg_id_temp=0
		rs1_temp=0
		w_val_temp=0
		if(IR[0].stall==0 and IR[0].isnull==False):
			IR[0].instruction=fetch(pc)
			IR[0].pc=copy.deepcopy(pc)
			#print(IR[1].isnull)
			IR[0].isnull=False
			#print(IR[1].isnull)
			if(hashmap.find(IR[0].pc)!=-1):
				IR[0].target_loaded = True
				pc = hashmap.find(IR[0].pc)-1#since this gets +1 after this iteration
				print("Used branch target buffer",file=debugf)
		
		if (IR[1].isFlushed == False and IR[1].stall==0 and IR[1].isnull==False):
			print("decode instruction",file=debugf)
			IR[1]=decode3(copy.deepcopy(IR[1]))
			if(IR[1].isLoad or IR[1].isStore):
				total_dfinst+=1
			if(IR[1].isALU):
				total_aluinst+=1
			if(IR[1].isJump or IR[1].isBranchInstruction):
				total_ctrlinst+=1	
			print("adda,addb,addc,",IR[1].address_a,IR[1].address_b,IR[1].address_c,file=debugf)
			print("now we are here,IR[1].RA",binary(IR[1].RA),file=debugf)
			#print(" IR[1] ",IR[1].isFlushed,IR[1].stall,IR[1].isnull,IR[1].instruction,IR[1].ins_type,file=debugf)
		if (IR[2].isFlushed == False and IR[2].stall==0 and IR[2].isnull==False):
			print('execute instruction',binary(IR[2].RA),binary(IR[2].RB),file=debugf)
			total_executions+=1
			#print("reg[8] before alu",binary(reg[8]),file=debugf)
			#print("before alu IR[2].RA",binary(IR[2].RA),"alu_op",IR[2].ALU_OP,file=debugf)
			IR[2] = alu(copy.deepcopy(IR[2]))
			#print("reg[8] after ALU,",binary(reg[8]),file=debugf)
			print("Value in RZ: ",binary(IR[2].RZ),file=debugf)
			if(IR[2].branchTaken==True):# dont know the use of controlHazard function
				flush()
				print("*************************",file=debugf)
				print("**flushed**",file=debugf)
				print("*************************",file=debugf)
				pc=iag(IR[2].pc_select, IR[2].pc_enable, IR[2].inc_select, IR[2].immediate, IR[2].RA,IR[2].pc)
				loop_runner_for_last_instruction = 0
				if(hashmap.find(IR[2].pc)==-1):
					hashmap.update(IR[2].pc,pc)
			#else: pc=pc+1	
				#print('pc updated in IR[2] condition to ',pc,IR[2].isFlushed,IR[2].isnull,IR[2].stall,"hhhhhhhhhhhhhhhhhhhhhhhh",file=debugf)
			if(IR[2].branchTaken==False and IR[2].target_loaded == True):
				flush()
				print("*************************",file=debugf)
				print("**flushed**",file=debugf)
				print("*************************",file=debugf)
				pc = IR[2].pc
		if IR[3].isFlushed == False and IR[3].stall==0 and IR[3].isnull==False:	
			#for i in range(32):
    				#print(i," ",binary(reg[i]),file=debugf)
			#print('MEM acces instruction')
			#print("Mem access instruction",IR[3].ins_type,IR[3].mem_write,IR[3].mem_read,IR[3].pc,file=debugf)
			#reg_id_temp,rs1_temp,w_val_temp
			#print("reg[8] before memwr",binary(reg[8]),file=debugf)
			#print("IR[3].RY in memwr",binary(IR[3].RY),file=debugf)
			IR[3] = mem_read_write(copy.deepcopy(IR[3]))  ## function split from RW function
			#print("IR[3].RY in memwr",binary(IR[3].RY),file=debugf)
			#print("reg[8] after memwr",binary(reg[8]),file=debugf)
			#IR[3].RY=w_val_temp
			if(IR[3].isLoad==True) :
				if(IR[1].address_a ==   IR[3].address_c):
					IR[1].RY=IR[3].RY
				if(IR[1].address_b ==   IR[3].address_c):
					IR[1].RY=IR[3].RY
		#print("here reg[8] is",binary(reg[8]),file=debugf)
		#print((IR[1].address_a),(IR[1].address_b),(IR[1].address_c),IR[1].pc,"xxxxxxxxxxxx",file=debugf)
		#print((IR[2].address_a),(IR[2].address_b),(IR[2].address_c),"yyyyyyyyyyyy",file=debugf)
		#print((IR[3].address_a),(IR[3].address_b),(IR[3].address_c),IR[3].pc,"ZZZZZZZZZZZZZ",file=debugf)			
		# print("IR[3].RY",IR[3].RY,file=debugf)			
        ##### Check hazard
		ForwardDependency_MtoE()
		ForwardDependencyMtoM()
		ForwardDependency_EtoE()
		stall_temp=DataDependencyStall()
		temp=PIP_REG()
		temp=PIP_REG()
		IR.insert(0,copy.deepcopy(temp))
		IR[0].stall=stall_temp
		temp2=IR.pop()
		# print(IR[2].address_a,IR[2].address_b,IR[2].address_c,"hello",file=debugf)
		
		#if(temp2.ins_type=="SB"):
    			#print(binary(temp2.RA),binary(temp2.RB),binary(temp2.RZ),temp2.branchTaken,temp2.pc,temp2.ALU_OP,"hjhjhjhjh",file=debugf)
		#print("and here reg[8] is",binary(reg[8]),file=debugf)			
		if(temp2.isnull==False and temp2.isFlushed == False):
			#print('reg_write was done:value',binary(temp2.RY),"at id",temp2.reg_id,file=debugf)
			reg_write(copy.deepcopy(temp2))       ## functions split from RW function
		#print("and and here reg[8] is",binary(reg[8]),file=debugf)			
	
		#print(stall_temp,len(machine_code),IR[2].branchTaken)
		if(stall_temp==0 and pc!=len(machine_code) and IR[3].branchTaken==False):
		   pc=pc+1
		#print('pc before if',pc)
		if(pc==len(machine_code) or pc==0):
			loop_runner_for_last_instruction+=1
			#print("holahup",loop_runner_for_last_instruction)
			IR[0].isnull=True
		else:
			IR[0].isnull=False
		clk+=1
		#print("clock" ,clk,file=debugf)
		#print("x1",binary(reg[1]),"x10",binary(reg[10]))
		if(knob3):	
			print("clock" ,clk,file=Regout)
			print("*************************",file=Regout)
			for i in range(32):
    				print("x"+str(i)+" = "+str(binary(reg[i])),file=Regout,end=", ")
			print("\n")
			print("*************************",file=Regout)
		if(knob4):
			print("========CLOCK============" ,clk,file=pipout)
			print("*************************",file=pipout)
			for i in range(4):
				print("----------------",file=pipout)
				print("||","Registor"+str(i),"||",file=pipout)
				print("----------------",file=pipout)
				print("Instruction MC ",IR[i].instruction,end=" ,",file=pipout)
				print("RA "+str(binary(IR[i].RA)),"RB "+str(binary(IR[i].RB)),"RZ "+str(binary(IR[i].RZ)) ,file=pipout,sep=" , ")
				print("AddressA "+str(IR[i].address_a),"AddressB "+str(IR[i].address_b),"AddressC "+str(IR[i].address_c) ,file=pipout,sep=" , ")
				print("immediate "+str(IR[i].immediate),"ALU_OP "+str(IR[i].ALU_OP),"b_select "+str(IR[i].b_SELECT) ,file=pipout,sep=" , ")
				print("pc_select "+str(IR[i].pc_select),"inc_select "+str(IR[i].inc_select),"Branch taken "+str(IR[i].branchTaken) ,file=pipout,sep=" , ")					
				print("mem_read "+str(IR[i].mem_read),"mem_write "+str(IR[i].mem_write),"no of bits r/w "+str(IR[i].mem_qty) ,file=pipout,sep=" , ")
				print("reg id "+str(IR[i].reg_id),"Target loaded "+str(IR[i].target_loaded),"Is Jump "+str(IR[i].isJump) ,file=pipout,sep=" , ")

			print("\n")
			print("*************************",file=pipout)
		if(knob5!=-1):
			for i in range(4):
				if(IR[i].pc==knob5):
					print("========CLOCK============" ,clk,file=Knob5out)
					print("*************************",file=Knob5out)
					print("----------------",file=Knob5out)
					print("||","Registor"+str(i),"||",file=Knob5out)
					print("----------------",file=Knob5out)
					print("Instruction MC ",IR[i].instruction,end=" ,",file=Knob5out)
					print("RA "+str(binary(IR[i].RA)),"RB "+str(binary(IR[i].RB)),"RZ "+str(binary(IR[i].RZ)) ,file=Knob5out,sep=" , ")
					print("AddressA "+str(IR[i].address_a),"AddressB "+str(IR[i].address_b),"AddressC "+str(IR[i].address_c) ,file=Knob5out,sep=" , ")
					print("immediate "+str(IR[i].immediate),"ALU_OP "+str(IR[i].ALU_OP),"b_select "+str(IR[i].b_SELECT) ,file=Knob5out,sep=" , ")
					print("pc_select "+str(IR[i].pc_select),"inc_select "+str(IR[i].inc_select),"Branch taken "+str(IR[i].branchTaken) ,file=Knob5out,sep=" , ")					
					print("mem_read "+str(IR[i].mem_read),"mem_write "+str(IR[i].mem_write),"no of bits r/w "+str(IR[i].mem_qty) ,file=Knob5out,sep=" , ")
					print("reg id "+str(IR[i].reg_id),"Target loaded "+str(IR[i].target_loaded),"Is Jump "+str(IR[i].isJump) ,file=Knob5out,sep=" , ")
					print("\n")
					print("*************************",file=Knob5out)
	print("• Stat1: Total number of cycles:  ",clk,file=outfile)
	print("• Stat2: Total instructions executed including reexecution of same instruction",total_executions,file=outfile)
	print("• Stat3: CPI",clk/total_executions,file=outfile)
	print("• Stat4: Number of Data-transfer (load and store) instructions executed",total_dfinst,file=outfile)
	print("• Stat5: Number of ALU instructions executed",total_aluinst,file=outfile)
	print("• Stat6: Number of Control instructions executed",total_ctrlinst,file=outfile)
	print("• Stat7: Number of stalls/bubbles in the pipeline",stalls_data_hazard+2*ctrl_hazard,file=outfile)
	print("• Stat8: Number of data hazards ",data_hazard,file=outfile)
	print("• Stat9: Number of control hazards",ctrl_hazard,file=outfile)
	print("• Stat10: Number of branch mispredictions",branch_miss_predict,file=outfile)#pradyumn add here
	print("• Stat11: Number of stalls due to data hazards",stalls_data_hazard,file=outfile)
	print("• Stat12: Number of stalls due to control hazards",0,file=outfile)  	 
			
			
			
			
			
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
			print("inside EtoE-1",file=debugf)
			data_hazard+=1
			IR[1].RA = IR[2].RZ
			IR[1].RB = IR[2].RZ
		if (IR[1].address_a == IR[2].address_c):#rd 0f exmem = rs1 of id_ex
			print("inside EtoE-2",file=debugf)
			data_hazard+=1
			IR[1].RA = IR[2].RZ
			return
		if (IR[1].address_b == IR[2].address_c):#rd of exmem = rs2 of id_ex
			print("inside EtoE- 3",file=debugf) 
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
			print( "inside 1 MtoE" ,file=debugf)
			data_hazard+=1
			IR[1].RA = IR[3].RY
			IR[1].RB = IR[3].RY
			return
		if (IR[1].address_a == IR[3].address_c):
			print( "inside 2 MtoE",file=debugf )
			data_hazard+=1
			IR[1].RA = IR[3].RY
			return
		if (IR[1].address_b == IR[3].address_c):
			print( "inside 3 MtoE" ,file=debugf)
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
				print ("MtoM",file=debugf) 
				data_hazard+=1
				IR[2].RB = IR[3].RY
				print("reg MEM_WB",IR[3].RY,debugf)
				return
			return
def DataDependencyStall():
	global stalls_data_hazard
	if(IR[2].isnull==True or IR[1].isnull==True):
			return 0
	#if(Stall_knob==0):
        	#eturn 0
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
	global ctrl_hazard
	ctrl_hazard+=1
	IR[0]=PIP_REG()
	IR[1]=PIP_REG()
	IR[0].isFlushed = True
	IR[1].isFlushed = True
    
run()

#print(reg[3],reg[4])
