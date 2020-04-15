from dataclasses import dataclass


@dataclass
class PIP_REG:# buffer reg between deccode and execute 
	def __init__(self, pc):
		self.pc=pc
    pc:int=0
	RA:int
	RB:int
	RZ:int
	immediate:int
	ALU_OP:int 
    B_SELECT:int# used in alu, tells whether to take imm or register
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
			if IR[i].state==5:
				IR.pop()
				temp=PIP_REG(pc)
				IR.append(temp)
			IR[i].nextstep()
			##### Check hazards
		for i in range(min(clk,5)):
			


