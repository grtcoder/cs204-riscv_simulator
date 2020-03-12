
def binary(arr):
    sum=0
    for i in range(len(arr)):
        sum+=arr[i](2*(len(arr)-1-i))
    return sum       

SIZE = 1<<63

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
        m /= 2
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
    while n>0:
        if n%2:
            val += "1"
        else:
            val += "0"
        k = int(n/2)
        n = int(k)
    string = "".join(reversed(val))
    return string

reg=[]*32

def alu(machine_code):
    # I-format
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
    bge_funct3 = [0,0,0]
    
    blt_op = [1,1,0,0,0,1,1]
    blt_funct3 = [1,0,0]

    # U-format
    auipc_op = [0,0,1,0,1,1,1]

    lui_op = [0,1,1,0,1,1,1]

    # UJ-format
    jal_op = [1,1,0,1,1,1]

    
    if(machine_code[25:32]==ld_op and machine_code[17:20]==ld_funct3):
        return toBinary(binary(machine_code[0:7]) + reg[binary(machine_code[12:17])])
    if(machine_code[25:32]==lh_op and machine_code[17:20]==lh_funct3):
        return toBinary(binary(machine_code[0:7]) + reg[binary(machine_code[12:17])])
    if(machine_code[25:32]==lw_op and machine_code[17:20]==lw_funct3):
        return toBinary(binary(machine_code[0:7]) + reg[binary(machine_code[12:17])])
    if(machine_code[25:32]==jalr_op and machine_code[17:20]==jalr_funct3):
        return toBinary(binary(machine_code[0:7]) + reg[binary(machine_code[12:17])])
    
    if(machine_code[25:32]==sb_op and machine_code[17:20]==sb_funct3):
        return toBinary(binary(machine_code[20:25]) + (2**5) * binary(machine_code[0:7]) + reg[binary(machine_code[12:17])])
    if(machine_code[25:32]==sw_op and machine_code[17:20]==sw_funct3):
        return toBinary(binary(machine_code[20:25]) + (2**5) * binary(machine_code[0:7]) + reg[binary(machine_code[12:17])])
    if(machine_code[25:32]==sd_op and machine_code[17:20]==sd_funct3):
        return toBinary(binary(machine_code[20:25]) + (2**5) * binary(machine_code[0:7]) + reg[binary(machine_code[12:17])])      
    if(machine_code[25:32]==sh_op and machine_code[17:20]==sh_funct3):
        return toBinary(binary(machine_code[20:25]) + (2**5) * binary(machine_code[0:7]) + reg[binary(machine_code[12:17])])

    if(machine_code[25:32]==beq_op and machine_code[17:20]==beq_funct3):
        if(reg[binary(machine_code[12:17])] == reg[binary(machine_code[7:12])]):
            return 1
        return 0
    if(machine_code[25:32]==bne_op and machine_code[17:20]==bne_funct3):
        if(reg[binary(machine_code[12:17])] != reg[binary(machine_code[7:12])]):
            return 1
        return 0
    if(machine_code[25:32]==bge_op and machine_code[17:20]==bge_funct3):
        if(reg[binary(machine_code[12:17])] >= reg[binary(machine_code[7:12])]):
            return 1
        return 0
    if(machine_code[25:32]==blt_op and machine_code[17:20]==blt_funct3):
        if(reg[binary(machine_code[12:17])] < reg[binary(machine_code[7:12])]):
            return 1
        return 0

    # if(machine_code[25:32]==)
    # auipc, jal, lui remaining
