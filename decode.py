def decode(instruction):#instruction comes as array of bits
    #control signals
    b_select = -1
    ALU_op = -1 
    mem_read = -1
    mem_write = -1
    reg_write = -1
    memqty = -1
    pc_enable = 1 
    pc_select = 1
    inc_select = 0
    type=""
    # R-format ###### to add more
    R_code=[0,1,1,0,0,1,1]
    add_funct7=[0,0,0,0,0,0,0]
    sub_funct7=[0,1,0,0,0,0,0]
    and_funct7=[0,0,0,0,0,0,0]
    or_funct7=[0,0,0,0,0,0,0]
    sll_funct7=[0,0,0,0,0,0,0]
    slt_funct7=[0,0,0,0,0,0,0]
    sra_funct7=[0,1,0,0,0,0,0]
    srl_funct7=[0,0,0,0,0,0,0]
    xor_funct7=[0,0,0,0,0,0,0]
    mul_funct7=[0,0,0,0,0,0,1]
    div_funct7=[0,0,0,0,0,0,1]
    rem_funct7=[0,0,0,0,0,0,1]


    add_funct3=[0,0,0]
    sub_funct3=[0,0,0]
    and_funct3=[1,1,1]
    or_funct3=[1,1,0]
    sll_funct3=[0,0,1]
    slt_funct3=[0,1,0]
    sra_funct3=[1,0,1]
    srl_funct3=[1,0,1]
    xor_funct3=[1,0,0]
    mul_funct3=[0,0,0]
    div_funct3=[1,0,0]
    rem_funct3=[1,1,0]
    # I-format
    I_code_load = [0,0,0,0,0,1,1]
    I_code_arith = [0,0,1,0,0,1,1]
    I_code_jalr = [1,1,0,0,1,1,1]
    lb_funct3 = [0,0,0]
    ld_funct3 = [0,1,1]
    lh_funct3 = [0,0,1]
    lw_funct3 = [0,1,0]    
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
        funct3=instruction[17:20]
        if funct3==lb_funct3:
            memqty=8
        elif funct3==lh_funct3:
            memqty=16
        elif funct3==lw_funct3:
            memqty=32
        elif funct3==ld_funct3:
            memqty=64
        ALU_op=0
    elif opcode==I_code_jalr:
        type="jalr"
        mem_read=0
        mem_write=0
        reg_write=1
        b_select=1
        ALU_op=0
    elif opcode==S_code:
        type="S"
        mem_read=0
        mem_write=1
        reg_write=0
        b_select=1
        ALU_op=0
        funct3=instruction[17:20]
        if funct3==sb_funct3:
            memqty=8
        elif funct3==sh_funct3:
            memqty=16
        elif funct3==sw_funct3:
            memqty=32
        elif funct3==sd_funct3:
            memqty=64
    elif opcode==SB_code:
        b_select=1
        type="SB"
        mem_read=0
        mem_write=0
        reg_write=0
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
        type='auipc'
        mem_read=0
        mem_write=0
        reg_write=1
        b_select=1
    elif opcode==lui_op:
        type='lui'
        mem_read=0
        mem_write=0
        reg_write=1
        b_select=1
    elif opcode==UJ_code:
        type="jal"
        b_select=1
        mem_read=0
        mem_write=0
        reg_write=1
    return type,b_select,ALU_op,mem_read,mem_write,reg_write,memqty,pc_enable,pc_select,inc_select
    