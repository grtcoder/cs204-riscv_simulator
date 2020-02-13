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
opcodes={
    "add":["0110011",'R'],
    "and":["0110011",'R'],
    "or": ["0110011",'R'],
    "sll":["0110011",'R'],
    "slt":["0110011",'R'],
    "sra":["0110011",'R'],
    "srl":["0110011",'R'],
    "sub":["0110011",'R'],
    "xor":["0110011",'R'],
    "mul":["0110011",'R'],
    "div":["0110011",'R'],
    "rem":["0110011",'R']
}
