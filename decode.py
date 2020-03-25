SIZE = 1<<32
SIZE -= 1

LIM= 1<<32

MAXP=1<<31
MAXP -= 1

def binary(arr):
    sum=0
    ch=1
    for i in range(len(arr)):
        sum+=arr[i]*(2**(len(arr)-1-i))
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
reg=[]*32
def decode(machine_code):#return pc_enable, pc_select, and inc_select for iag
    pc_enable = 1 #for iag
    pc_select = 1 #for iag, except for jalr, pc_select is always 0
    inc_select = 0 #for iag, only 1 for branch and jump instructions
    
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
        if(reg[binary(machine_code[12:17])] == reg[binary(machine_code[7:12])]):
            inc_select = 1
    if(machine_code[25:32]==bne_op and machine_code[17:20]==bne_funct3):
        if(reg[binary(machine_code[12:17])] != reg[binary(machine_code[7:12])]):
            inc_select = 1
    if(machine_code[25:32]==bge_op and machine_code[17:20]==bge_funct3):
        if(reg[binary(machine_code[12:17])] >= reg[binary(machine_code[7:12])]):
            inc_select = 1
    if(machine_code[25:32]==blt_op and machine_code[17:20]==blt_funct3):
        if(reg[binary(machine_code[12:17])] < reg[binary(machine_code[7:12])]):
            inc_select = 1

    return [pc_select,pc_enable,inc_select]