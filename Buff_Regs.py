from dataclasses import dataclass





@dataclass
class REG_IF_ID:#buffer reg between fetch and decode
    pc: int=0
    mc: int=0
    enable: int = 0
    enable2: int = 1
class REG_ID_EX:# buffer reg between deccode and execute
    pc: int=0
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
    #above boolean will help us easily identify and take action for hazards
    enable:int=0
	enable2:int=1
class REG_EX_MEM:#buffer reg bet execute and memory access
    pc: int=0
	RA:int
	RB:int
	RZ:int
	immediate:int
	ALU_OP:int 
    B_SELECT:int
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
	isJump:bool=False#jal and jalr

    enable:int=0
	enable2:int=1
class REG_MEM_WB: # buffer reg bet mem acc and mem write back
    pc: int=0
	RY:int
    RF_WRITE:int
    adrs_c:int
	branchTaken:bool=False
	isBranchInstruction:bool=False
	isLoad:bool=False
	isStore:bool=False
	isALU:bool=False
	isJump:bool=False#jal and jalr

    enable:int=0
	enable2:int=1
