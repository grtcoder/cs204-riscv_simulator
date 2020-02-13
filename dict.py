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
pc=0
# def isvalid(command):
#     True if command is found in dict, false otherwise
# def update_pc(command,inp1): 
while not terminate:
    v=firstoc(lines[pc],' ')
    command,inp=lines[pc][:v],lines[pc][v+1:]
    #isvalid()
    input_arguments=inp.split(',')
    if(len(input_arguments)>3):
        print('Too many Arguments')
        sys.exit()
    
f.close()
#testing
instructions = [[0]*32]*32
#funct 7:
for i in range(7):
    instructions[0][i]=0
    instructions[1][i]=0
    instructions[2][i]=0
    instructions[3][i]=0
    instructions[4][i]=0
    instructions[6][i]=0
    instructions[8][i]=0

instructions[5][1]=1
instructions[7][1]=1 
instructions[9][6]=1 
instructions[10][6]=1 
instructions[11][6]=1 

#funct 3:    

opcodes={
    "add":instructions[0],
    "and":instructions[1],
    "or":instructions[2],
    "sll":instructions[3],
    "slt":instructions[4],
    "sra":instructions[5],
    "srl":instructions[6],
    "sub":instructions[7],
    "xor":instructions[8],
    "mul":instructions[9],
    "div":instructions[10],
    "rem":instructions[11]
    }
