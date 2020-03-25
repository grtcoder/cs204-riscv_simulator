# import sys
import json
from labels import labelize
# filename=sys.argv[1]#commands like python <file_name> (<risc-v code path>) => sys.argv[1]
# if(not filename.endswith('.asm')):
#     print("This file format is invalid")
#     sys.exit()
# f=open(filename,'r+')
jfile=open("instruction_set.json","r+")
# lines=f.read().splitlines()
# terminate=False
def firstoc(str,char):#for splitting command from the first space
    for i in range(len(str)):
        if str[i]==char:
            return i
    return -1
typ={#for type of instruction
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
def type(command):
    if command in typ.keys():
        return typ[command]
    return "Z"
instruction_set=json.load(jfile)
def is_valid_reg(str1):
    for i in range(27):
        if "x"+str(i)==str1:
            return 1
    return 0
def get_bin(str1,len):
    str1=str1.replace('x','')
    num= str1
    binary  = bin(int(num)).replace("0b", "")
    while len(binary)<len:
          binary = '0'+binary
    return binary
def ifINT(val):
    try:
        int(val)
        return True
    except ValueError:
        return False       
def split(str):
    return [char for char in str]
def is_valid_label(str,labels):
    if str in labels.keys():
        return 1
    return 0
def check(commands,inputs,labels):
    errors=[]  #typewise machine code generator
    for i in range(len(commands)):#moving command by command
        if len(inputs[i])>3:#no command has more than 3 fields
            errors.append("Line "+str(i)+" Too many arguments")
        if type(commands[i])=="R":
            if len(inputs[i])<3:# exactly 3 fields are present in R type instruction
                errors.append("Line "+str(i)+" Too few arguments")
            if (not is_valid_reg(inputs[i][0])) or (not is_valid_reg(inputs[i][1])) or (not is_valid_reg(inputs[i][2])):
                errors.append("Line "+str(i)+" Invalid register names")
        elif type(commands[i])=="I":
            if len(inputs[i])<3:
                errors.append("Line "+str(i)+"Too few arguments")
            if (not is_valid_reg(inputs[i][0])) or (not is_valid_reg(inputs[i][1])):
                errors.append("Line "+str(i)+" Invalid register names")
            if not ifINT(inputs[i][2]):
                errors.append("Line "+str(i)+" Not a valid integer")
            else:
                val=int(inputs[i][2])
                if val>2047 and val<-2048:
                    errors.append("Line "+str(i)+" Immediate field not inn range")
        elif type(commands[i])=="S":
            if len(inputs[i])<2:
                errors.append("Line "+str(i)+" Too few arguments")
            if len(inputs[i])>2:
                errors.append("Line "+str(i)+" Too many arguments")
            if (not is_valid_reg(inputs[i][0])):
                errors.append("Line "+str(i)+" Invalid register names")
            s=inputs[i][1]
            temp=s[s.find('('):s.find(')')+1]
            if not is_valid_reg(temp):
                errors.append("Line "+str(i)+" Invalid register names")
            offset=s[:s.find('(')+1]
            offset.strip()
            if not ifINT(offset):
                errors.append("Line "+str(i)+" immediate field is not a valid integer")
            if offset>2047 and offset<-2048:
                errors.append("Line "+str(i)+" Immediate field not inn range")
        elif type(commands[i])=="SB":
            if len(inputs[i])<3:
                errors.append("Line "+str(i)+"Too few arguments")
            if (not is_valid_reg(inputs[i][0])) or (not is_valid_reg(inputs[i][1])):
                errors.append("Line "+str(i)+"Invalid register names")
            if not is_valid_label(inputs[i][1],dict):
                errors.append("Line "+str(i)+"Undeclared label")
        elif type(commands[i])=="U":
            if len(inputs[i])<2:
                errors.append("Line "+str(i)+"Too few arguments")
            if len(inputs[i])>2:
                errors.append("Line "+str(i)+"Too many arguments")
            if (not is_valid_reg(inputs[i][0])):
                    errors.append("Line "+str(i)+"Invalid register name")
            comp=pow(2,19)
            offset=inputs[i][1]
            offset.strip()
            if not ifINT(offset):
                errors.append("Line "+str(i)+"immediate field is not a valid integer")
            if int(offset)>comp and int(offset)<-comp-1:
                errors.append("Line "+str(i)+"Immediate field not in range")
        elif type(commands[i])=="U":
            if len(inputs[i])<2:
                errors.append("Line "+str(i)+"Too few arguments")
            if len(inputs[i])>2:
                errors.append("Line "+str(i)+"Too many arguments")
            if not is_valid_reg(inputs[i][0]):
                errors.append("Line "+str(i)+"Invalid register name")
            comp=pow(2,19)
            offset=inputs[i][1]
            offset.strip()
            if not ifINT(offset):
                errors.append("Line "+str(i)+"immediate field is not a valid integer")
            if int(offset)>comp and int(offset)<-comp-1:
                errors.append("Line "+str(i)+"Immediate field not in range")
        else: 
            errors.append("Line "+str(i)+"Undefined operation")
            
    if len(errors)==0:
        errors.append("All good!!")
    return errors
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
def execute_error_chk(lines):
    commands,inputs=split_data(lines)
    labels=labelize(lines)
    return check(commands,inputs,labels)
