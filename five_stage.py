def fetch(addr):
       instruction=MEM[addr:addr+4]
       ######################## add pc updation herei
       return instruction
def decode_(instruction):#instruction comes as array of bits
    #control signals
    b_select=-1
    ALU_op=-1 
    mem_read=-1
    mem_write=-1
    reg_write=-1
    memqty=-1
    y_select=-1
    type=""
    # R-format ###### to add more
    R_code=[0,1,1,0,0,1,1]
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
    # I-format
    I_code_load = [0,0,0,0,0,1,1]
    I_code_arith = [0,0,1,0,0,1,1]
    I_code_jalr = [1,1,0,0,1,1,1]
    jalr_funct3 = [0,0,0]
    lb_funct3 = [0,0,0]
    ld_funct3 = [0,1,1]
    lh_funct3 = [0,0,1]
    lw_funct3 = [0,1,0]    
    jalr_funct3 = [0,0,0]
    addi_funct3 = [0,0,0]
    andi_funct3 = [1,1,1]
    ori_funct3 = [1,1,0]

    # S-format
    S_code = [0,1,0,0,0,1,1]
    sb_funct3 = [0,0,0]
    sw_funct3 = [0,1,0]
    sh_funct3 = [0,0,1]
    sd_funct3 = [0,1,1]


    # SB-format
    SB_code= [1,1,0,0,0,1,1]
    beq_funct3 = [0,0,0]
    bne_funct3 = [0,0,1]
    bge_funct3 = [1,0,1]
    blt_funct3 = [1,0,0]
    # U-format
    auipc_op = [0,0,1,0,1,1,1]
    lui_op = [0,1,1,0,1,1,1]
    # UJ-format
    UJ_code = [1,1,0,1,1,1,1] 
    opcode=instruction[25:32]
    if opcode==R_code:
        b_select=0
        type="R"
        mem_read=0
        mem_write=0
        reg_write=1
        y_select=0
        funct7=instruction[0:7]
        funct3=instruction[17:20]
        if funct7==add_funct7 and funct3==add_funct3:
            ALU_op=0
        elif funct7==sub_funct7 and funct3==sub_funct3:
            ALU_op=1
        elif funct7==and_funct7 and funct3==and_funct3:
            ALU_op=2
        elif funct7==or_funct7 and funct3==or_funct3:
            ALU_op=3
        elif funct7==sll_funct7 and funct3==sll_funct3:
            ALU_op=4
        elif funct7==slt_funct7 and funct3==slt_funct3:
            ALU_op=5
        elif funct7==sra_funct7 and funct3==sra_funct3:
            ALU_op=6
        elif funct7==srl_funct7 and funct3==srl_funct3:
            ALU_op=7
        elif funct7==xor_funct7 and funct3==xor_funct3:
            ALU_op=8
        elif funct7==mul_funct7 and funct3==mul_funct3:
            ALU_op=9
        elif funct7==div_funct7 and funct3==div_funct3:
            ALU_op=10
        elif funct7==rem_funct7 and funct3==rem_funct3:
            ALU_op=11
    elif opcode==I_code_arith:
        type="I"
        mem_read=0
        mem_write=0
        reg_write=1
        b_select=1
        y_select=0
        funct3=instruction[17:20]
        if funct3==addi_funct3:
            ALU_op=0
        elif funct3==andi_funct3:
            ALU_op=2
        elif funct3==ori_funct3:
            ALU_op=3
    elif opcode==I_code_load:###### review...
        type="I"
        mem_read=1
        mem_write=0
        reg_write=1
        b_select=1
        y_select=1
        ALU_op=0
    elif opcode==I_code_jalr:
        type="I"
        mem_read=0
        mem_write=0
        reg_write=1
        b_select=1
        y_select=2
        ALU_op=0
    elif opcode==S_code:
        type="S"
        mem_read=0
        mem_write=1
        reg_write=0
        b_select=1
        y_select=0
        ALU_op=0
        funct3=instruction[17:20]
        if funct3==sb_funct3:
            memqty=1
        elif funct3==sh_funct3:
            memqty=2
        elif funct3==sw_funct3:
            memqty=3
        elif funct3==sd_funct3:
            memqty=4
    elif opcode==SB_code:
        b_select=1
        type="SB"
        mem_read=0
        mem_write=0
        reg_write=0
        memqty=0
        funct3=instruction[17:20]
        if funct3==beq_funct3:
            ALU_op=12
        elif funct3==bge_funct3:
            ALU_op=13
        elif funct3==blt_funct3:
            ALU_op=14
        elif funct3==bne_funct3:
            ALU_op=15
    elif opcode==auipc_op:
        type='U'
        mem_read=0
        mem_write=0
        reg_write=1

    elif opcode==lui_op:
        type='U'
        mem_read=0
        mem_write=0
        reg_write=1
    elif opcode==UJ_code:
        b_select=1