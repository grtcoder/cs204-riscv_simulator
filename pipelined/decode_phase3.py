from ALU_Phase3 import *
#from ALU_Phase3 import binary
#from ALU_Phase3 import reg,MEM
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
def decode3(instruction):  # instruction comes as array of bits
    #control signals
    pipreg=PIP_REG()
    pipreg.address_a=binary(reg[binary(instruction[12:17])])#rs1
    pipreg.address_b=binary(reg[binary(instruction[7:12])])#rs2
    pipreg.address_c=binary(reg[binary(instruction[20:25])])#rd
    b_select = -1
    ALU_op = -1
    mem_read = -1
    mem_write = -1
    reg_write = -1
    memqty = -1
    pc_enable = 1
    pc_select = 1
    inc_select = 0
    type = ""
    # R-format ###### to add more
    R_code = [0, 1, 1, 0, 0, 1, 1]
    add_funct7 = [0, 0, 0, 0, 0, 0, 0]
    sub_funct7 = [0, 1, 0, 0, 0, 0, 0]
    and_funct7 = [0, 0, 0, 0, 0, 0, 0]
    or_funct7  = [0, 0, 0, 0, 0, 0, 0]
    sll_funct7 = [0, 0, 0, 0, 0, 0, 0]
    slt_funct7 = [0, 0, 0, 0, 0, 0, 0]
    sra_funct7 = [0, 1, 0, 0, 0, 0, 0]
    srl_funct7 = [0, 0, 0, 0, 0, 0, 0]
    xor_funct7 = [0, 0, 0, 0, 0, 0, 0]
    mul_funct7 = [0, 0, 0, 0, 0, 0, 1]
    div_funct7 = [0, 0, 0, 0, 0, 0, 1]
    rem_funct7 = [0, 0, 0, 0, 0, 0, 1]
    add_funct3 = [0, 0, 0]
    sub_funct3 = [0, 0, 0]
    and_funct3 = [1, 1, 1]
    or_funct3  = [1, 1, 0]
    sll_funct3 = [0, 0, 1]
    slt_funct3 = [0, 1, 0]
    sra_funct3 = [1, 0, 1]
    srl_funct3 = [1, 0, 1]
    xor_funct3 = [1, 0, 0]
    mul_funct3 = [0, 0, 0]
    div_funct3 = [1, 0, 0]
    rem_funct3 = [1, 1, 0]
    # I-format
    I_code_load = [0, 0, 0, 0, 0, 1, 1]
    I_code_arith = [0, 0, 1, 0, 0, 1, 1]
    I_code_jalr = [1, 1, 0, 0, 1, 1, 1]
    lb_funct3 = [0, 0, 0]
    ld_funct3 = [0, 1, 1]
    lh_funct3 = [0, 0, 1]
    lw_funct3 = [0, 1, 0]
    addi_funct3 = [0, 0, 0]
    andi_funct3 = [1, 1, 1]
    ori_funct3 = [1, 1, 0]

    # S-format
    S_code    = [0, 1, 0, 0, 0, 1, 1]
    sb_funct3 = [0, 0, 0]
    sw_funct3 = [0, 1, 0]
    sh_funct3 = [0, 0, 1]
    sd_funct3 = [0, 1, 1]

    # SB-format
    SB_code    = [1, 1, 0, 0, 0, 1, 1]
    beq_funct3 = [0, 0, 0]
    bne_funct3 = [0, 0, 1]
    bge_funct3 = [1, 0, 1]
    blt_funct3 = [1, 0, 0]
    # U-format
    auipc_op = [0, 0, 1, 0, 1, 1, 1]
    lui_op = [0, 1, 1, 0, 1, 1, 1]
    # UJ-format
    UJ_code = [1, 1, 0, 1, 1, 1, 1]
    opcode = instruction[25:32]
    if opcode == R_code:
        pipreg.isALU=True
        b_select = 0
        type = "R"
        mem_read = 0
        mem_write = 0
        reg_write = 1
        funct7 = instruction[0:7]
        funct3 = instruction[17:20]
        if funct7 == add_funct7 and funct3 == add_funct3:
            ALU_op = 0
        elif funct7 == sub_funct7 and funct3 == sub_funct3:
            ALU_op = 1
        elif funct7 == and_funct7 and funct3 == and_funct3:
            ALU_op = 2
        elif funct7 == or_funct7 and funct3 == or_funct3:
            ALU_op = 3
        elif funct7 == sll_funct7 and funct3 == sll_funct3:
            ALU_op = 4
        elif funct7 == slt_funct7 and funct3 == slt_funct3:
            ALU_op = 5
        elif funct7 == sra_funct7 and funct3 == sra_funct3:
            ALU_op = 6
        elif funct7 == srl_funct7 and funct3 == srl_funct3:
            ALU_op = 7
        elif funct7 == xor_funct7 and funct3 == xor_funct3:
            ALU_op = 8
        elif funct7 == mul_funct7 and funct3 == mul_funct3:
            ALU_op = 9
        elif funct7 == div_funct7 and funct3 == div_funct3:
            ALU_op = 10
        elif funct7 == rem_funct7 and funct3 == rem_funct3:
            ALU_op = 11
    elif opcode == I_code_arith:
        type = "I"
        pipreg.isALU=True
        mem_read = 0
        mem_write = 0
        reg_write = 1
        b_select = 1
        funct3 = instruction[17:20]
        if funct3 == addi_funct3:
            ALU_op = 0
        elif funct3 == andi_funct3:
            ALU_op = 2
        elif funct3 == ori_funct3:
            ALU_op = 3
    elif opcode == I_code_load:  # review...
        type = "I"
        pipreg.isLoad=True
        mem_read = 1
        mem_write = 0
        reg_write = 1
        b_select = 1
        funct3 = instruction[17:20]
        if funct3 == lb_funct3:
            memqty = 1
        elif funct3 == lh_funct3:
            memqty = 2
        elif funct3 == lw_funct3:
            memqty = 4
        elif funct3 == ld_funct3:
            memqty = 8
        ALU_op = 0
    elif opcode == I_code_jalr:
        type = "jalr"
        pipreg.isJump=True
        pc_select = 0
        inc_select = 1
        mem_read = 0
        mem_write = 0
        reg_write = 1
        b_select = 1
        ALU_op = 0
    elif opcode == S_code:
        type = "S"
        pipreg.isStore=True
        mem_read = 0
        mem_write = 1
        reg_write = 0
        b_select = 1
        ALU_op = 0
        funct3 = instruction[17:20]
        if funct3 == sb_funct3:
            memqty = 1
        elif funct3 == sh_funct3:
            memqty = 2
        elif funct3 == sw_funct3:
            memqty = 4
        elif funct3 == sd_funct3:
            memqty = 8
    elif opcode == SB_code:
        b_select = 0
        pipreg.isBranchInstruction=True
        type = "SB"
        mem_read = 0
        mem_write = 0
        inc_select = 1
        reg_write = 0
        funct3 = instruction[17:20]
        if funct3 == beq_funct3:
            ALU_op = 12
        elif funct3 == bge_funct3:
            ALU_op = 13
        elif funct3 == blt_funct3:
            ALU_op = 14
        elif funct3 == bne_funct3:
            ALU_op = 15
    elif opcode == auipc_op:
        type = 'auipc'
        #todo
        pipreg.isALU=True
        mem_read = 0
        mem_write = 0
        reg_write = 1
        b_select = 1
    elif opcode == lui_op:
        type = 'lui'
        #todo
        pipreg.isALU=True
        mem_read = 0
        mem_write = 0
        reg_write = 1
        b_select = 1
    elif opcode == UJ_code:
        type = "jal"
        pipreg.isJump=True
        b_select = 1
        inc_select = 1
        mem_read = 0
        mem_write = 0
        reg_write = 1
    pipreg.b_select=b_select
    pipreg.ALU_op=ALU_op
    pipreg.mem_read=mem_read
    pipreg.mem_write=mem_write
    pipreg.reg_write=reg_write
    pipreg.memqty=memqty
    pipreg.pc_enable=pc_enable
    pipreg.pc_select=pc_select
    pipreg.inc_select=inc_select
    pipreg.type=type
    pipreg.immediate=get_immediate(instruction, type)
    return pipreg
