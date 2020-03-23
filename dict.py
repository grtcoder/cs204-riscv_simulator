# import sys
import json
from bitstring import Bits
# filename=sys.argv[1]#commands like python <file_name> (<risc-v code path>) => sys.argv[1]
# if(not filename.endswith('.asm')):
#     print("This file format is invalid")
#     sys.exit()
# f=open(filename,'r+')
# jfile=open("instruction_set.json","r+")
# lines=f.read().splitlines()
terminate=False
def firstoc(str,char):#for splitting command from the first space
    for i in range(len(str)):
        if str[i]==char:
            return i
    return -1
type={#for type of instruction
    "add":"R", 
    "and":"R", 
    "sll":"R", 
    "slt":"R", 
    "sra":"R", 
    "srl":"R", 
    "sub":"R", 
    "xor":"R", 
    "mul":"R", 
    "div":"R", 
    "rem":"R",
    "or":"R",
    "addi":"I",
    "andi":"I",
    "ori":"I",
    "lb":"I", 
    "ld":"I", 
    "lh":"I", 
    "lw":"I", 
    "jalr":"I",
    "sb":"S", 
    "sw":"S", 
    "sd":"S", 
    "sh":"S",
    "beq":"SB", 
    "bne":"SB", 
    "bge":"SB", 
    "blt":"SB",
    "auipc":"U", 
    "lui":"U",
    "jal":"UJ"
}
def is_valid_reg(str1):
    for i in range(27):
        if "x"+str(i)==str1:
            return 1
    return 0
def get_bin(str1,length1):
    str1=str1.replace('x','')
    num= str1
    binary  = bin(int(num)).replace("0b", "")
    while len(binary)<length1:
             binary = '0'+binary
    return binary     
def get_binimm(str1,length1):
    str1=str1.replace('x','')
    num= int(str1)
    b = Bits(int=num, length=length1)
    # binary  = bin(int(num)).replace("0b", "")
    # while len(binary)<length1:
    #          binary = '0'+binary
    return b.bin      
def split(str):
    return [char for char in str]
def machine_code(command,inputs):
    mc=[]
    instruction_set=json.load(jfile) 
    instructions=[]   #typewise machine code generator
    # f=open('machine_code.mc','w+')
    for i in range(len(command)):#moving command by command
        if type[command[i]]=="R":
            # print("R")
            instruction=instruction_set[command[i]]
            temp=inputs[i]
            # if len(temp)<3:
            #    print("Very few arguments")
            #    sys.exit()
            rs1=''
            rs2=''
            rd=''
            rd=temp[0]
            rs1=temp[1]
            rs2=temp[2]
            instruction[32-12+1:32-7+1]=get_bin(rd,5)
            instruction[7:12]=get_bin(rs2,5)
            instruction[12:17]=get_bin(rs1,5)
            # print(len(instruction))
            # print(instruction)
        elif type[command[i]]=="I":
            # print("I")
            instruction=instruction_set[command[i]]
            temp=inputs[i]
            rs1=''
            rs2=''
            rd=''
            if len(temp) == 2 : # for stmts like ld lw etc
                rs1 = temp[1][temp[1].find("(")+1:temp[1].find(")")]
                imm = temp[1][0:temp[1].find("(")]
                rd= temp[0]
                instruction[32-12+1:32-7+1]=get_bin(rd,5)
                instruction[0:12]=get_binimm(imm,12)
                instruction[12:17]=get_bin(rs1,5)
                # print(len(instruction))
                # print(instruction)          
            if len(temp)==3:
                rs1=''
                imm=''
                rd=temp[0]
                rs1=temp[1]
                imm=temp[2]
                instruction[32-12+1:32-7+1]=get_bin(rd,5)
                instruction[0:12]=get_binimm(imm,12)
                instruction[12:17]=get_bin(rs1,5)
                # print(len(instruction))
                # print(instruction)
        elif type[command[i]]=="S":
            # print("S")
            instruction=instruction_set[command[i]]
            temp=inputs[i]
            rs1=''
            rs2=''
            rd=''
            if len(temp) == 2 : # for stmts like ld lw etc
                rs1 = temp[1][temp[1].find("(")+1:temp[1].find(")")]
                imm = temp[1][0:temp[1].find("(")]
                rs2= temp[0]
                bina = get_binimm(imm,12)
                instruction[0:7]   = bina[:7]#for imm
                instruction[20:25] = bina[7:12]# for imm
                instruction[12:17] =  get_bin(rs1,5)# for rs1
                instruction[7:12]  = get_bin(rs2,5)
                # print(len(instruction))
                # print(instruction)  
        elif type[command[i]]=="SB":
            # print("SB")
            instruction=instruction_set[command[i]]
            temp=inputs[i]
            rs1=''
            rs2=''
            rd=''
            if len(temp) == 3 : # for stmts like beq bge  etc
                rs1 = temp[1] 
                imm = temp[2]
                rs2= temp[0]
                bina = get_binimm(imm,13)
                instruction[0]= bina[1]
                instruction[25]=bina[2]
                instruction[1:7]   = bina[3:9]#for imm
                instruction[20:24] =bina[9:13]# for imm
                instruction[12:17] =get_bin(rs1,5)# for rs1
                instruction[7:12]  =get_bin(rs2,5)
                # print(len(instruction))
                # print(instruction)
        elif type[command[i]]=="U":
            # print("U")
            instruction=instruction_set[command[i]]
            temp=inputs[i]
            if len(temp) == 2 : # for stmts like ld lw etc
                rd = temp[0]
                imm = temp[1]
                bina = get_binimm(imm,32)
                instruction[0:20]   =bina[0:20]#for imm(remember imm is reverses ie highest bit is 0)
                instruction[21:26] =get_bin(rd,5)# for rs1
                # print(len(instruction))
                # print(instruction)  
        elif type[command[i]]=="UJ":
            # print("UJ")
            instruction=instruction_set[command[i]]
            temp=inputs[i]
            if len(temp) == 2 : # for stmts like ld lw etc
                rd = temp[0]
                imm = temp[1]
                bina = get_binimm(imm,21)
                instruction[0] = bina[1]
                instruction[12:20]   =bina[2:10]#for imm(remember imm is reverses ie highest bit is 0)
                instruction[11]= bina[10]
                instruction[1:11]=bina[11:21]
                instruction[21:26] =get_bin(rd,5)# for rs1
                print(len(instruction))
                print(instruction)
        instructions.append(instruction)
    return instructions 
commands=[]
inputs=[]
def split_data(lines):
    commands=[]
    inputs=[]
    for i in range(len(lines)):
        v=firstoc(lines[i],' ')
        command,inp=lines[i][:v],lines[i][v+1:]
        # if command not in instruction_set.keys():
        #     print("Unknown keyword")
        #     sys.exit()
        input_arguments=inp.split(',')
        # if(len(input_arguments)>3):
        #     print('Too many Arguments')
        #     sys.exit()
        for i in range(len(input_arguments)):
            input_arguments[i]=input_arguments[i].strip()
        commands.append(command)
        for x in range(len(input_arguments)):
            input_arguments[x]= input_arguments[x].strip()
        inputs.append(input_arguments)
    return commands,inputs
# for i in range(len(lines)):
#     v=firstoc(lines[i],' ')
#     command,inp=lines[i][:v],lines[i][v+1:]
#     # if command not in instruction_set.keys():
#     #     print("Unknown keyword")
#     #     sys.exit()
#     input_arguments=inp.split(',')
#     # if(len(input_arguments)>3):
#     #     print('Too many Arguments')
#     #     sys.exit()
#     commands.append(command)
#     for x in range(len(input_arguments)):
#           input_arguments[x]= input_arguments[x].strip()
#     inputs.append(input_arguments)
# machine_code(commands,inputs)
# f.close()
