from iag_dp import *
from labels import *
from Phase_1_complete import *
SIZE = 1<<32
SIZE -= 1

LIM= 1<<32

MAXP=1<<31
MAXP -= 1
# def split(word): 
#     return [int(char) for char in word]def



    
def write_from_memory(start, len, reg_id):
    print('write from',start, len, reg_id)
    for i in range(32):
        reg[reg_id][i] = 0
    # i = 0
    # while 1:
    for j in range(32):
        reg[reg_id][31-j] = MEM[start+j]
        # i += 8
        # if i>= len:
        #     break
def write_to_memory(start, len, reg_id):
    i = 0
    print('reg x22',int("".join(list(map(str,reg[22]))),2))
    print('write to,reg',start,int("".join(list(map(str,reg[reg_id]))),2))
    # while 1:
    for j in range(32):
        MEM[start+j] = reg[reg_id][31-j]
        # i += 8
        # if i>=len:
        #     break
def binary(arr):
    sum=0
    ch=1
    for i in range(len(arr)):
        sum+=(int(arr[i]))*(2**(len(arr)-1-i))
        if(sum>MAXP):
            ch=0
    if(ch==1):
        return sum
    else:
        return sum-LIM
def add(m):
    n = 0
    carr = 1
    pow = 1
    while m>0:
        sum = m%2 + carr
        carr = 0
        if sum==2:
            sum = 0
            carr = 1
        n += sum*pow
        pow *= 2
        m =int(m/2)
    n %= (SIZE+1)
    return n

def _2C(n):
    m = SIZE
    m = m^n 
    return add(m)

def toBinary(n):
    val = ""
    if n<0:
        n = _2C(-n)
    while n>0 or len(val)<32:
        if n%2:
            val += "1"
        else:
            val += "0"
        k = int(n/2)
        n = int(k)
    string = "".join(reversed(val))
    return string

# print(toBinary(10))

def decode(machine_code):#return pc_enable, pc_select, and inc_select for iag
    # print('decode code')

    pc_enable = 1 #for iag
    pc_select = 1 #for iag, except for jalr, pc_select is always 0
    inc_select = 0 #for iag, only 1 for branch and jump instructions
    machine_code = list(map(int, machine_code))
    jalr_op = [1,1,0,0,1,1,1]
    jalr_funct3 = [0,0,0]
    
    # SB-format
    beq_op = [1,1,0,0,0,1,1]
    beq_funct3 = [0,0,0]
    
    bne_op = [1,1,0,0,0,1,1]
    bne_funct3 = [0,0,1]
    
    bge_op = [1,1,0,0,0,1,1]
    bge_funct3 = [1,0,1]
    
    blt_op = [1,1,0,0,0,1,1]
    blt_funct3 = [1,0,0]

    jal_op = [1,1,0,1,1,1,1]

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

    # if(machine_code[25:32]==)
    # auipc, jal, lui remaining
    
    
    
    
    if(machine_code[25:32]==add_op and machine_code[17:20]==add_funct3 and machine_code[0:7]==add_funct7):      #add
        return toBinary(binary(reg[binary(machine_code[12:17])])+binary(reg[binary(machine_code[7:12])]))
    elif(machine_code[25:32]==add_op and machine_code[17:20]==add_funct3 and machine_code[0:7]==sub_funct7):    #sub
        return toBinary(binary(reg[binary(machine_code[12:17])])-binary(reg[binary(machine_code[7:12])]))                        
    elif(machine_code[25:32]==add_op and machine_code[17:20]==and_funct3 and machine_code[0:7]==add_funct7):    #and
        return toBinary(binary(reg[binary(machine_code[12:17])])&binary(reg[binary(machine_code[7:12])]))
    elif(machine_code[25:32]==add_op and machine_code[17:20]==or_funct3 and machine_code[0:7]==add_funct7):     #or
        return toBinary(binary(reg[binary(machine_code[12:17])])|binary(reg[binary(machine_code[7:12])]))
    elif(machine_code[25:32]==add_op and machine_code[17:20]==sll_funct3 and machine_code[0:7]==add_funct7):    #sll
        return toBinary(binary(reg[binary(machine_code[12:17])])*(2**(binary(reg[binary(machine_code[7:12])]))))
    elif(machine_code[25:32]==add_op and machine_code[17:20]==slt_funct3 and machine_code[0:7]==add_funct7):    #slt
        if(binary(reg[binary(machine_code[12:17])])<binary(reg[binary(machine_code[7:12])])):
            return 1
        return 0        
    elif(machine_code[25:32]==add_op and machine_code[17:20]==sra_funct3 and machine_code[0:7]==sub_funct7):    #sra
        return toBinary(int(binary(reg[binary(machine_code[12:17])])/(2**(binary(reg[binary(machine_code[7:12])])))))
    elif(machine_code[25:32]==add_op and machine_code[17:20]==sra_funct3 and machine_code[0:7]==add_funct7):    #srl
        return toBinary(abs(int(binary(reg[binary(machine_code[12:17])])/(2**(binary(reg[binary(machine_code[7:12])]))))))
    elif(machine_code[25:32]==add_op and machine_code[17:20]==xor_funct3 and machine_code[0:7]==add_funct7):    #xor
        return toBinary(binary((reg[binary(machine_code[12:17])]))^binary(reg[binary(machine_code[7:12])]))
    elif(machine_code[25:32]==add_op and machine_code[17:20]==add_funct3 and machine_code[0:7]==mul_funct7):    #mul
        return toBinary(binary(reg[binary(machine_code[12:17])])*binary(reg[binary(machine_code[7:12])]))
    elif(machine_code[25:32]==add_op and machine_code[17:20]==xor_funct3 and machine_code[0:7]==mul_funct7):    #div
        return toBinary(int(binary(reg[binary(machine_code[12:17])])/binary(reg[binary(machine_code[7:12])])))  
    elif(machine_code[25:32]==addi_op and machine_code[17:20]==add_funct3):                                     #addi
        tt23="".join(map(str, machine_code[0:12]))
        tt23=twosCom_binDec(tt23,12)
        return toBinary(binary(reg[binary(machine_code[12:17])])+tt23)
#         return toBinary(binary(reg[binary(machine_code[12:17])])+binary(machine_code[0:12]))      
    elif(machine_code[25:32]==addi_op and machine_code[17:20]==andi_funct3):                                    #andi
        return toBinary(binary(reg[binary(machine_code[12:17])])&binary(machine_code[0:12]))
    elif(machine_code[25:32]==addi_op and machine_code[17:20]==or_funct3):                                      #ori
        return toBinary(binary(reg[binary(machine_code[12:17])])|binary(machine_code[0:12]))
    elif(machine_code[25:32]==add_op and machine_code[17:20]==or_funct3 and machine_code[0:7]==mul_funct7):     #rem
        x=binary(reg[binary(machine_code[12:17])])%(binary(reg[binary(machine_code[7:12])]))
        if(x<0):
            x-=binary(reg[binary(machine_code[7:12])])
        return toBinary(x) 


def RW(machine_code, aluVal,PC):
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

    reg_id = binary(machine_code[20:25])
    start = binary(aluVal)
    # print('start', start,aluVal)
    reg_str = binary(machine_code[7:12])

    if(machine_code[25:32]==ld_op and machine_code[17:20]==ld_funct3):
        # NOT SUPPORTED
        print("Error, 64 bit operation")
        return
    if(machine_code[25:32]==lb_op and machine_code[17:20]==lb_funct3):
        write_from_memory(start,8,reg_id)
    if(machine_code[25:32]==lh_op and machine_code[17:20]==lh_funct3):
        write_from_memory(start,16,reg_id)
    if(machine_code[25:32]==lw_op and machine_code[17:20]==lw_funct3):
        write_from_memory(start,32,reg_id)
    if(machine_code[25:32]==jalr_op and machine_code[17:20]==jalr_funct3):
        reg[reg_id] = aluVal
    
    if(machine_code[25:32]==sb_op and machine_code[17:20]==sb_funct3):
        write_to_memory(start,8,reg_str)
    if(machine_code[25:32]==sw_op and machine_code[17:20]==sw_funct3):
        write_to_memory(start,32,reg_str)
    if(machine_code[25:32]==sd_op and machine_code[17:20]==sd_funct3):
        # NOT SUPPORTED
        print("Error, 64 bit operation")
        return
    if(machine_code[25:32]==sh_op and machine_code[17:20]==sh_funct3):
        write_to_memory(start,16,reg_str)
    if(machine_code[25:32]==add_op and machine_code[17:20]==add_funct3 and machine_code[0:7]==add_funct7):      #add
        reg[binary(machine_code[20:25])]=aluVal
        # print(reg)
    elif(machine_code[25:32]==add_op and machine_code[17:20]==add_funct3 and machine_code[0:7]==sub_funct7):    #sub
        reg[binary(machine_code[20:25])]=aluVal                       
    elif(machine_code[25:32]==add_op and machine_code[17:20]==and_funct3 and machine_code[0:7]==add_funct7):    #and
        reg[binary(machine_code[20:25])]=aluVal
    elif(machine_code[25:32]==add_op and machine_code[17:20]==or_funct3 and machine_code[0:7]==add_funct7):     #or
        reg[binary(machine_code[20:25])]=aluVal
    elif(machine_code[25:32]==add_op and machine_code[17:20]==sll_funct3 and machine_code[0:7]==add_funct7):    #sll
        reg[binary(machine_code[20:25])]=aluVal
    elif(machine_code[25:32]==add_op and machine_code[17:20]==slt_funct3 and machine_code[0:7]==add_funct7):    #slt
         reg[binary(machine_code[20:25])]=toBinary(int(aluVal[0]))  
    elif(machine_code[25:32]==add_op and machine_code[17:20]==sra_funct3 and machine_code[0:7]==sub_funct7):    #sra
        reg[binary(machine_code[20:25])]=aluVal
    elif(machine_code[25:32]==add_op and machine_code[17:20]==sra_funct3 and machine_code[0:7]==add_funct7):    #srl
        reg[binary(machine_code[20:25])]=aluVal
    elif(machine_code[25:32]==add_op and machine_code[17:20]==xor_funct3 and machine_code[0:7]==add_funct7):    #xor
        reg[binary(machine_code[20:25])]=aluVal
    elif(machine_code[25:32]==add_op and machine_code[17:20]==add_funct3 and machine_code[0:7]==mul_funct7):    #mul
        reg[binary(machine_code[20:25])]=aluVal
    elif(machine_code[25:32]==add_op and machine_code[17:20]==xor_funct3 and machine_code[0:7]==mul_funct7):    #div
        reg[binary(machine_code[20:25])]=aluVal  
    elif(machine_code[25:32]==addi_op and machine_code[17:20]==add_funct3):                                     #addi                                                                  #addi
        reg[binary(machine_code[20:25])]=aluVal      
    elif(machine_code[25:32]==addi_op and machine_code[17:20]==andi_funct3):                                    #andi
        reg[binary(machine_code[20:25])]=aluVal
    elif(machine_code[25:32]==addi_op and machine_code[17:20]==or_funct3):                                      #ori
        reg[binary(machine_code[20:25])]=aluVal
    elif(machine_code[25:32]==add_op and machine_code[17:20]==or_funct3 and machine_code[0:7]==mul_funct7):     #rem
        reg[binary(machine_code[20:25])]=aluVal    
    elif(machine_code[25:32]==lui_op):                                                                          #lui            
        for i in range(20):
            reg[binary(machine_code[20:25])][i]=machine_code[i]
        for i in range(20,32):
            reg[binary(machine_code[20:32])][i]=0    
    
    if(machine_code[25:32]==jal_op):
        # PC = []*32                                         # comment when merged
        reg[binary(machine_code[20:25])] = toBinary(PC)                # Global PC

    if(machine_code[25:32]==auipc_op):
        imm = binary(machine_code[0:20])
        imm = imm<<12
        reg[binary(machine_code[20:25])] = toBinary(imm + PC)
    reg[0]=[0 for x in range(32)]
    return reg_id
def twosCom_binDec(bin, digit):
        while len(bin)<digit :
                bin = '0'+bin
        if bin[0] == '0':
                return int(bin, 2)
        else:
                return -1 * (int(''.join('1' if x == '0' else '0' for x in bin), 2) + 1)

def get_immediate(machine_code):
    machine_code = list(map(int, machine_code))
    beq_op = [1,1,0,0,0,1,1]
    beq_funct3 = [0,0,0]
    
    bne_op = [1,1,0,0,0,1,1]
    bne_funct3 = [0,0,1]
    
    bge_op = [1,1,0,0,0,1,1]
    bge_funct3 = [1,0,1]
    
    blt_op = [1,1,0,0,0,1,1]
    blt_funct3 = [1,0,0]

    jal_op = [1,1,0,1,1,1,1]

    jalr_op = [1,1,0,0,1,1,1]
    jalr_funct3 = [0,0,0]

    imm = 0
    # print(machine_code,jal_op)
    if(machine_code[25:32] == beq_op):
        if(machine_code[17:20] == beq_funct3 or machine_code[17:20] == bge_funct3 or machine_code[17:20]==blt_funct3 or machine_code[17:20] == bne_funct3):
            immt=[0 for x in range(0,13)]
            immt[0]=machine_code[0]#immt[12]
            immt[1]=machine_code[24]#immt[11]
            immt[2:8]=machine_code[1:7]   #[10:5]
            immt[8:12]= machine_code[20:24]#[4:1]
            immt[12]=0
            # for i in range(13):
            #     imm *= 2
            #     if immt[i] == 1:
            #         imm += 1
            # if(machine_code[17:20] == beq_funct3):
            #     print('imm',imm)
            t23="".join(map(str, immt))
            imm=twosCom_binDec(t23,13)
            # if(machine_code[17:20] == beq_funct3):
            #     print('imm',imm)
    if(machine_code[25:32] == jal_op):
            # print('mac code',machine_code[0:20])
            immt=[0 for x in range(0,21)]
            immt[0]=machine_code[0]#immt[20]
            immt[9]=machine_code[11]#immt[11]
            immt[1:9]=machine_code[12:20]  #[19:12]
            immt[10:20]= machine_code[1:11]#[10:1]
            immt[20]=0
            # print(immt,'immt')
            t23="".join(map(str, immt))
            imm=twosCom_binDec(t23,21)
            # for i in range(21):
            #     imm *= 2
            #     if immt[i] == 1:
            #         imm += 1
            # print(imm,'imm')
#           
#             txyz=""
#             t23=txyz.join(immt)
#             imm=int(t23,2)

    return imm
def run(machine_code,temp):
    # temp=copy.deepcopy(PC)
    MC = []
    for i in range(32-len(machine_code)):
        MC.append(int(0))
    for i in range(len(machine_code)):
        MC.append(machine_code[i])
    # print(MC)
    pc_select,pc_enable,inc_select=decode(MC)
    res=str(alu(MC))
    # print(res)
    reg_id=RW(MC,split(res),temp)
    imm = get_immediate(MC)
    # print('my imm',imm)
    # print(pc_select,pc_enable,inc_select,imm,reg[reg_id],temp)
    return iag(pc_select,pc_enable,inc_select,imm,reg[reg_id],temp)
    # res=str(alu(machine_code))
    # print(res)
    # reg_id=RW(machine_code,split(res),temp)
    # imm = get_immediate(machine_code)
    # return iag(pc_select,pc_enable,inc_select,imm,reg[reg_id],temp)

def decimalToBinary(n):  
    return bin(n).replace("0b", "")
def split(word):
    x=[]
    for i in range(len(word)):
        if word[i]=='0':
            x.append(int(0))
        else:
            x.append(int(1))
    return x
f=open('testing.asm','r+')
data=f.read().split('\n')
data1=mc_gen(data).split('\n')
#print(data1)
# print(data1)
def full_run(data1,PC):
    if(data1!=['']):
        data2=[]
        for i in data1:
            z=toBinary(int(i,0))
            data2.append(z)
        print(len(data2))
        while PC<len(data2):
            temp=copy.deepcopy(PC)
            print(PC,data2[temp])
            PC=run(data2[temp],temp)
            if(PC==0):
                break
    # print(reg[3],reg[4],sep='\t')
full_run(data1,0)
# for i in range(0,300,32):
#     for j in range(32):
#         print(MEM[i+j],end='')
#     print('')
# print('x16',reg[16])
# print('x1',reg[1])
f.close()
#uncomment below loop to print values after sorting
# for x in range(5):
#     abcde=""
#     abcde=abcde.join(list(map(str,MEM[2016+x*32:2016+(x+1)*32])) )
#     abcde = "".join(reversed(abcde))
#     print(int(abcde,2))
# abcde=""
# abcde=abcde.join(list(map(str,reg[8])) )
# abcde = "".join(abcde)
# print('regx8',int(abcde,2))