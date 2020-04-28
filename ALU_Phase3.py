SIZE = 1<<32
SIZE -= 1

LIM= 1<<32
#shifted it here from phase3 coz its used here in alu 
reg = [[0 for x in range(0, 32)] for x in range(0, 32)]
MEM = [0 for x in range(0, 100000)]
# reg = []
# MEM = []
MAXP=1<<31
MAXP -= 1
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
    
    if ins_type == "I"  or ins_type=="jalr":
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

    if ins_type == "UJ" or ins_type=="jal" :    # same as above
        immt=[0 for x in range(0,21)]
        immt[0]=machine_code[0]#immt[20]
        immt[9]=machine_code[11]#immt[11]
        immt[1:9]=machine_code[12:20]  #[19:12]
        immt[10:20]= machine_code[1:11]#[10:1]
        immt[20]=0
        t23="".join(map(str, immt))
        imm=twosCom_binDec(t23,21)
        #print('UJ format in get_imm',imm)

    return imm
def alu(machine_code, alu_op, b_select, ins_type):
    machine_code = list(map(int, machine_code))
    value1 = binary(reg[binary(machine_code[12:17])])
    value2 = binary(reg[binary(machine_code[7:12])])
    print('value 1 ', value1 ,'value 2 ',  value2, 'alu_op', alu_op)
    if b_select :
        value2 = get_immediate(machine_code, ins_type)
    
    if alu_op == 0 :
        return toBinary ( value1 + value2 )
    
    if alu_op == 1 :
        return toBinary ( value1 - value2 )
    
    if alu_op == 2 :
        return toBinary ( value1 & value2 )
    
    if alu_op == 3 :
        return toBinary ( value1 | value2 )
    
    if alu_op == 4 :
        return toBinary ( value1 << value2 )  
    
    if alu_op == 5 :
        if value1 < value2 :
            return 1
        return 0
    
    if alu_op == 6 :
        return toBinary ( int ( value1 >> value2 ) )

    if alu_op == 7 :
        return toBinary ( abs ( int ( value1 >> value2 ) ) )
    
    if alu_op == 8 :
        return toBinary ( value1 ^ value2 )

    if alu_op == 9 :
        return toBinary ( value1 * value2 )

    if alu_op == 10 :
        return toBinary ( int ( value1 / value2 ) )
    
    if alu_op == 11 :
        rem = value1 % value2
        if rem < 0 :
            rem -= value2
        return toBinary ( rem )

    #ankit:did below in a hurry as it was incomplete check later
    if(alu_op==12):
        print("hola")
        print(binary(reg[binary(machine_code[12:17])]))
        print(binary(reg[binary(machine_code[7:12])]))
        if(binary(reg[binary(machine_code[12:17])]) == binary(reg[binary(machine_code[7:12])])):
           
            return 1
        
        return 0
    if(alu_op==15):
    #if(machine_code[25:32]==bne_op and machine_code[17:20]==bne_funct3):
        if(binary(reg[binary(machine_code[12:17])] )!= binary(reg[binary(machine_code[7:12])])):
            return 1
        return 0
    if(alu_op==13):
    # if(machine_code[25:32]==bge_op and machine_code[17:20]==bge_funct3):
        if(binary(reg[binary(machine_code[12:17])]) >=binary( reg[binary(machine_code[7:12])])):
            return 1
        return 0
    if(alu_op==14):
    #if(machine_code[25:32]==blt_op and machine_code[17:20]==blt_funct3):
        if(binary(reg[binary(machine_code[12:17])]) < binary(reg[binary(machine_code[7:12])])):
            return 1
        return 0
    #adding this because jal vgerah mein it was returning "NONE"
    return 0
#Operation Keys for ALU 0 - + 1 - - 2 - and 3 - or 4 - logical left shift 5- less than 6 - arithmetic right
#  7 - logical right 8 - xor 9 - multiply 10 - divide 11 - modulus 
# 12 - equal 13 - greater than equal to 14 - less than 15 - not equal to