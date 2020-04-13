def twosCom_binDec(bin, digit):
        while len(bin)<digit :
                bin = '0'+bin
        if bin[0] == '0':
                return int(bin, 2)
        else:
                return -1 * (int(''.join('1' if x == '0' else '0' for x in bin), 2) + 1)

def get_immediate(machine_code, ins_type):
    machine_code = list(map(int, machine_code))

    imm = 0

    # if(machine_code[25:32] == beq_op):
    #     if(machine_code[17:20] == beq_funct3 or machine_code[17:20] == bge_funct3 or machine_code[17:20]==blt_funct3 or machine_code[17:20] == bne_funct3):
    #         immt=[0 for x in range(0,13)]
    #         immt[0]=machine_code[0]#immt[12]
    #         immt[1]=machine_code[24]#immt[11]
    #         immt[2:8]=machine_code[1:7]   #[10:5]
    #         immt[8:12]= machine_code[20:24]#[4:1]
    #         immt[12]=0
    #         t23="".join(map(str, immt))
    #         imm=twosCom_binDec(t23,13)
    # if(machine_code[25:32] == jal_op):
    #         immt=[0 for x in range(0,21)]
    #         immt[0]=machine_code[0]#immt[20]
    #         immt[9]=machine_code[11]#immt[11]
    #         immt[1:9]=machine_code[12:20]  #[19:12]
    #         immt[10:20]= machine_code[1:11]#[10:1]
    #         immt[20]=0
    #         t23="".join(map(str, immt))
    #         imm=twosCom_binDec(t23,21)
    
    if ins_type == "I" :
        tt23="".join(map(str, machine_code[0:12]))
        tt23=twosCom_binDec(tt23,12)
        imm = tt23
    
    if ins_type == "S" :
        imm_field = machine_code[0:7]
        for i in range(20, 25) :
            imm_field.append(machine_code[i])
        tt23="".join(map(str, imm_field))
        tt23=twosCom_binDec(tt23,12)
        imm = tt23
    
    if ins_type == "SB" : # same as above
        immt=[0 for x in range(0,13)]
        immt[0]=machine_code[0]#immt[12]
        immt[1]=machine_code[24]#immt[11]
        immt[2:8]=machine_code[1:7]   #[10:5]
        immt[8:12]= machine_code[20:24]#[4:1]
        immt[12]=0
        t23="".join(map(str, immt))
        imm=twosCom_binDec(t23,13)
    # if ins_type == "U" :    NOT NEEDED ?

    if ins_type == "UJ" :    # same as above
        immt=[0 for x in range(0,21)]
        immt[0]=machine_code[0]#immt[20]
        immt[9]=machine_code[11]#immt[11]
        immt[1:9]=machine_code[12:20]  #[19:12]
        immt[10:20]= machine_code[1:11]#[10:1]
        immt[20]=0
        t23="".join(map(str, immt))
        imm=twosCom_binDec(t23,21)

    return imm
