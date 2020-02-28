import sys
import json
filename=sys.argv[1]#commands like python <file_name> (<risc-v code path>) => sys.argv[1]
if(not filename.endswith('.asm')):
    print("This file format is invalid")
    sys.exit()
f=open(filename,'r+')
jfile=open("instruction_set.json","r+")
lines=f.read().splitlines()
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
instruction_set=json.load(jfile)
def is_valid_reg(str1):
    for i in range(27):
        if "x"+str(i)==str1:
            return 1
    return 0
def split(str):
    return [char for char in str]
def machine_code(command,inputs):#typewise machine code generator
    f=open('machine_code.mc','w+')
    for i in range(len(command)):#moving command by command
        if type[command[i]]=="R":
            instruction=instruction_set[command[i]]
            temp=inputs[i]
            if len(temp)<3:
                print("Very few arguments")
                sys.exit()
            rs1=''
            rs2=''
            rd=''
            if is_valid_reg(temp[0]) and is_valid_reg(temp[1]) and is_valid_reg(temp[2]):
                rd=temp[0]
                rs1=temp[1]
                rs2=temp[2]
            instruction[7:12]=split(rd)
            print(instruction)
commands=[]
inputs=[]
for i in range(len(lines)):
    v=firstoc(lines[i],' ')
    command,inp=lines[i][:v],lines[i][v+1:]
    if command not in instruction_set.keys():
        print("Unknown keyword")
        sys.exit()
    input_arguments=inp.split(',')
    if(len(input_arguments)>3):
        print('Too many Arguments')
        sys.exit()
    commands.append(command)
    inputs.append(input_arguments)
machine_code(commands,inputs)
f.close()