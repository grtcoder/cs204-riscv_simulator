import sys
filename=sys.argv[1]#commands like python <file_name> (<risc-v code path>) => sys.argv[1]
if(not filename.endswith('.asm')):
    print("This file format is invalid")
    sys.exit()
f=open(filename,'r+')
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
def setline(type_,arguments):#for making machine code of a line
    if type_=="R":

pc=0
# def isvalid(command):
#     True if command is found in dict, false otherwise
# def update_pc(command,inp1): 
while not terminate:
    v=firstoc(lines[pc],' ')
    command,inp=lines[pc][:v],lines[pc][v+1:]
    if command not in opcodes.keys():
        print("Unknown keyword")
        break
    input_arguments=inp.split(',')
    if(len(input_arguments)>3):
        print('Too many Arguments')
        sys.exit()
    setline(type[command],input_arguments)
f.close()