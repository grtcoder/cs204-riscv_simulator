from iag_dp import *
from labels import *
from Phase_1_complete import *
def fetch():
    instruction=MEM[] #fill this
    return instruction
def decode():
    pc_enable = 1 #for iag
    pc_select = 1 #for iag, except for jalr, pc_select is always 0
    inc_select = 0 #for iag, only 1 for branch and jump instructions
    machine_code = list(map(int, machine_code))
    # jalr_op = [1,1,0,0,1,1,1]
    # jalr_funct3 = [0,0,0]
    
    # # SB-format
    # beq_op = [1,1,0,0,0,1,1]
    # beq_funct3 = [0,0,0]
    
    # bne_op = [1,1,0,0,0,1,1]
    # bne_funct3 = [0,0,1]
    
    # bge_op = [1,1,0,0,0,1,1]
    # bge_funct3 = [1,0,1]
    
    # blt_op = [1,1,0,0,0,1,1]
    # blt_funct3 = [1,0,0]

    # jal_op = [1,1,0,1,1,1,1]
    
    if(machine_code[25:32] == jal_op):
        inc_select = 1
    if(machine_code[25:32]==jalr_op and machine_code[17:20]==jalr_funct3):
        pc_select = 0
        inc_select = 1
        
    if(machine_code[25:32]==beq_op and machine_code[17:20]==beq_funct3):
        if(binary(reg[binary(machine_code[12:17])] )== binary(reg[binary(machine_code[7:12])])):
            inc_select = 1
    if(machine_code[25:32]==bne_op and machine_code[17:20]==bne_funct3):
        if(binary(reg[binary(machine_code[12:17])]) !=binary( reg[binary(machine_code[7:12])])):
            inc_select = 1
    if(machine_code[25:32]==bge_op and machine_code[17:20]==bge_funct3):
        # print(reg[binary(machine_code[12:17])],reg[binary(machine_code[7:12])])
        if(binary(reg[binary(machine_code[12:17])]) >= binary(reg[binary(machine_code[7:12])])):
            inc_select = 1
    if(machine_code[25:32]==blt_op and machine_code[17:20]==blt_funct3):
        if(binary(reg[binary(machine_code[12:17])]) <binary( reg[binary(machine_code[7:12])]) ):
            inc_select = 1

    return [pc_select,pc_enable,inc_select]
def alu(machine_code):
    machine_code = list(map(int, machine_code))
    add_op=[0,1,1,0,0,1,1]
    addi_op=[0,0,1,0,0,1,1]
    add_funct7=[0,0,0,0,0,0,0]
    sub_funct7=[0,1,0,0,0,0,0]
    mul_funct7=[0,0,0,0,0,0,1]
    add_funct3=[0,0,0]
    and_funct3=[1,1,1]
    or_funct3=[1,1,0]
    sll_funct3=[0,0,1]
    slt_funct3=[0,1,0]
    sra_funct3=[1,0,1]
    xor_funct3=[1,0,0]
    andi_funct3=[1,1,1]
   # I-format
    lb_op = [0,0,0,0,0,1,1]
    lb_funct3 = [0,0,0]

    ld_op = [0,0,0,0,0,1,1]
    ld_funct3 = [0,1,1]
    
    lh_op = [0,0,0,0,0,1,1]
    lh_funct3 = [0,0,1]
    
    lw_op = [0,0,0,0,0,1,1]
    lw_funct3 = [0,1,0]
    
    jalr_op = [1,1,0,0,1,1,1]
    jalr_funct3 = [0,0,0]

    # S-format
    sb_op = [0,1,0,0,0,1,1]
    sb_funct3 = [0,0,0]
    
    sw_op = [0,1,0,0,0,1,1]
    sw_funct3 = [0,1,0]
    
    sh_op = [0,1,0,0,0,1,1]
    sh_funct3 = [0,0,1]
    
    sd_op = [0,1,0,0,0,1,1]     # I or S ? ? ? ? ?
    sd_funct3 = [0,1,1]
    
    # SB-format
    beq_op = [1,1,0,0,0,1,1]
    beq_funct3 = [0,0,0]
    
    bne_op = [1,1,0,0,0,1,1]
    bne_funct3 = [0,0,1]
    
    bge_op = [1,1,0,0,0,1,1]
    bge_funct3 = [1,0,1]
    
    blt_op = [1,1,0,0,0,1,1]
    blt_funct3 = [1,0,0]

    # U-format
    auipc_op = [0,0,1,0,1,1,1]

    lui_op = [0,1,1,0,1,1,1]

    # UJ-format
    jal_op = [1,1,0,1,1,1,1]

    if(machine_code[25:32]==lb_op and machine_code[17:20]==lb_funct3):
        return toBinary(binary(machine_code[0:12]) + binary(reg[binary(machine_code[12:17])]))
    if(machine_code[25:32]==ld_op and machine_code[17:20]==ld_funct3):
        return toBinary(binary(machine_code[0:12]) + binary(reg[binary(machine_code[12:17])]))
    if(machine_code[25:32]==lh_op and machine_code[17:20]==lh_funct3):
        return toBinary(binary(machine_code[0:12]) + binary(reg[binary(machine_code[12:17])]))
    if(machine_code[25:32]==lw_op and machine_code[17:20]==lw_funct3):
        return toBinary(binary(machine_code[0:12]) + binary(reg[binary(machine_code[12:17])]))
    if(machine_code[25:32]==jalr_op and machine_code[17:20]==jalr_funct3):
        return toBinary(binary(machine_code[0:12]) + binary(reg[binary(machine_code[12:17])]))
     
    if(machine_code[25:32]==sb_op and machine_code[17:20]==sb_funct3):
        return toBinary(binary(machine_code[20:25]) + (2**5) * binary(machine_code[0:7]) + binary(reg[binary(machine_code[12:17])]))
    if(machine_code[25:32]==sw_op and machine_code[17:20]==sw_funct3):
        return toBinary(binary(machine_code[20:25]) + (2**5) * binary(machine_code[0:7]) + binary(reg[binary(machine_code[12:17])]))
    if(machine_code[25:32]==sd_op and machine_code[17:20]==sd_funct3):
        return toBinary(binary(machine_code[20:25]) + (2**5) * binary(machine_code[0:7]) + binary(reg[binary(machine_code[12:17])]))      
    if(machine_code[25:32]==sh_op and machine_code[17:20]==sh_funct3):
        return toBinary(binary(machine_code[20:25]) + (2**5) * binary(machine_code[0:7]) + binary(reg[binary(machine_code[12:17])]))

    if(machine_code[25:32]==beq_op and machine_code[17:20]==beq_funct3):
        if(binary(reg[binary(machine_code[12:17])]) == binary(reg[binary(machine_code[7:12])])):
            return 1
        return 0
    if(machine_code[25:32]==bne_op and machine_code[17:20]==bne_funct3):
        if(binary(reg[binary(machine_code[12:17])] )!= binary(reg[binary(machine_code[7:12])])):
            return 1
        return 0
    if(machine_code[25:32]==bge_op and machine_code[17:20]==bge_funct3):
        if(binary(reg[binary(machine_code[12:17])]) >=binary( reg[binary(machine_code[7:12])])):
            return 1
        return 0
    if(machine_code[25:32]==blt_op and machine_code[17:20]==blt_funct3):
        if(binary(reg[binary(machine_code[12:17])]) < binary(reg[binary(machine_code[7:12])])):
            return 1
        return 0
