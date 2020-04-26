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
# print(machine_code)
#print("xx",len(machine_code))		
def fetch(pc):
	MC = []
	print("pc",pc,file=debugf)
	for i in range(32-len(machine_code[pc])):
		MC.append(int(0))
	for i in range(len(machine_code[pc])):
		MC.append(int(machine_code[pc][i]))
	print("fetched instruction at pc: ",pc,file=debugf)
	print(MC,file=debugf)
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
	#if target pc is loaded and we do not take that branch, we need to flush IR[0] and IR[1] and set pc to IR[3].pc
IR=[]
data_hazard=0
ctrl_hazard=0
stalls_data_hazard=0
branch_miss_predict=0
just_fetched = 0
done = 0

#Data Stalling code starts here

def stall_run():
	knob3= int(input("Enable(1)/disable(0) printing values in the register file at the end of each cycle:  "))
	knob4=int(input("Enable(1)/disable(0) printing information in the pipeline registers at the end of each cycle: "))
	knob5=int(input("Print information in the pipeline registers for instruction no(-1 to disable): "))
	clk=0
	global data_hazard
	global ctrl_hazard
	global stalls_data_hazard
	global branch_miss_predict

	a=PIP_REG()
	for i in range(4):
		b=copy.deepcopy(a)
		IR.append(b)
	pc=0
	stall_temp=0
	total_executions=0
	total_ctrlinst=0
	total_dfinst=0
	total_aluinst=0
	loop_runner_for_last_instruction=0
	IR[0].isnull = False
	hashmap = branch_target_buffer()
	while(1 and loop_runner_for_last_instruction<4):			
		# Stall_Program()

		print("r3: ",reg[3],file=debugf)

		if(IR[0].stall==0 and IR[0].isnull==False):
			IR[0].instruction=fetch(pc)
			# print("Fetched instruction: ",IR[0].ins_type)
			IR[0].pc=copy.deepcopy(pc)
			IR[0].isnull=False
			if(hashmap.find(IR[0].pc)!=-1):
				IR[0].target_loaded = True
				pc = hashmap.find(IR[0].pc)-1#since this gets +1 after this iteration
				print("Used branch target buffer",file=debugf)
		
		if (len(IR)>1 and IR[1].isFlushed == False and IR[1].isnull==False):
			IR[1]=decode3(copy.deepcopy(IR[1]))
			if(IR[1].isLoad or IR[1].isStore):
				total_dfinst+=1
			if(IR[1].isALU):
				total_aluinst+=1
			if(IR[1].isJump or IR[1].isBranchInstruction):
				total_ctrlinst+=1
			print("\t\t\t\t\t\tdecoding",file=debugf)
		
		if (len(IR)>2 and IR[2].isFlushed == False and IR[2].isnull==False):
			total_executions+=1
			IR[2] = alu(copy.deepcopy(IR[2]))
			if(IR[2].branchTaken==True):
				flush()
				pc=iag(IR[2].pc_select, IR[2].pc_enable, IR[2].inc_select, IR[2].immediate, IR[2].RA,IR[2].pc)
				if(hashmap.find(IR[2].pc)==-1):
					hashmap.update(IR[2].pc,pc)
			if(IR[2].branchTaken==False and IR[2].target_loaded == True):
				flush()
				pc = IR[2].pc
		
		if (len(IR)>3 and IR[3].isFlushed == False and IR[3].isnull==False):
			IR[3] = mem_read_write(copy.deepcopy(IR[3]))  
		Stall_Program()
		
		for i in range(3):
			IR[i].stall = max(IR[i].stall-1,0)
		print("size: ",len(IR),file=debugf)
		for i in range(len(IR)):
			if(IR[0].stall == 0):
				break
			if (IR[i].stall == 0 and IR[i].isnull == False and IR[i].isFlushed == False):
				if(i == 0 or i == 4):
					break
				print("Adding buffer register ",i,file=debugf)
				temp = PIP_REG()
				IR.insert(i,temp)
				break
		temp2=IR.pop()
		if(temp2.isnull==False):				
			print('reg_write was done:value',(temp2.RY),"at id",temp2.reg_id,file=debugf)
			reg_write(copy.deepcopy(temp2))	
		# Stall_Program()
		# Stall_Program()
		stall_temp = IR[0].stall #if fetch is stalled, then stall other phases
		if(stall_temp == 0):
			temp=PIP_REG()
			IR.insert(0,copy.deepcopy(temp))
			IR[0].stall=0
		
		for i in range(len(IR)):
			print("Address ",i,IR[i].address_a,IR[i].address_b,IR[i].address_c,end = ' ',file=debugf)
			print("Stall time: ",IR[i].stall,file=debugf)
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

		print("clock" ,clk,file=debugf)
		print("*************************",file=debugf)
		print("*************************",file=debugf)
	print("• Stat1: Total number of cycles:  ",clk,file=outfile)
	print("• Stat2: Total instructions executed including re-execution of same instruction",total_executions,file=outfile)
	print("• Stat3: CPI",clk/total_executions,mfile=outfile)
	print("• Stat4: Number of Data-transfer (load and store) instructions executed",total_dfinst,file=outfile)
	print("• Stat5: Number of ALU instructions executed",total_aluinst,file=outfile)
	print("• Stat6: Number of Control instructions executed",total_ctrlinst,file=outfile)
	print("• Stat7: Number of stalls/bubbles in the pipeline",stalls_data_hazard,file=outfile)#pradyumn add flushes due to control_hazard here
	print("• Stat8: Number of data hazards ",data_hazard,file=outfile)
	print("• Stat9: Number of control hazards",ctrl_hazard,file=outfile)
	print("• Stat10: Number of branch mispredictions",branch_miss_predict,file=outfile)#pradyumn add here
	print("• Stat11: Number of stalls due to data hazards",stalls_data_hazard,file=outfile)
	print("• Stat12: Number of stalls due to control hazards",0,file=outfile)  

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
			print("inside EtoE-1",file=debugf)
			data_hazard+=1
			IR[1].stall = 3 #stall this instruction
			IR[0].stall = 3
			return 
		if (IR[1].address_a == IR[2].address_c):#rd 0f exmem = rs1 of id_ex
			print("inside EtoE-2",file=debugf)
			data_hazard+=1
			IR[1].stall = 3
			IR[0].stall = 3
			return 
		if (IR[1].address_b == IR[2].address_c):#rd of exmem = rs2 of id_ex
			print("inside EtoE- 3",file=debugf) 
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
			print( "inside 1 MtoE",file=debugf )
			data_hazard+=1
			IR[1].stall = max(IR[1].stall,2)
			IR[0].stall = max(IR[0].stall,2)
			return 
		if (IR[1].address_a == IR[3].address_c):
			print( "inside 2 MtoE",file=debugf )
			data_hazard+=1
			IR[1].stall = max(IR[1].stall,2)
			IR[0].stall = max(IR[0].stall,2)
			return 
		if (IR[1].address_b == IR[3].address_c):
			print( "inside 3 MtoE" ,file=debugf)
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
			print ("MtoM",file=debugf) 
			data_hazard+=1
			for i in range(3):
				IR[i].stall = max(IR[i].stall,2)
			print("reg MEM_WB",IR[3].RY,file=debugf)
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
	gloabl ctrl_hazard
	ctrl_hazard+=1
	IR[0]=PIP_REG()
	IR[1]=PIP_REG()
	IR[0].isFlushed = True
	IR[1].isFlushed = True
# Stall_knob = map(int,input("Data Forwarding(0) or Stalling(1) ?"))
stall_run()
print(reg[10],file=debugf)
