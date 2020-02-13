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

opcodes={
    "add":"0110011",
     "and":"0110011",
      "or":"0110011",
       "sll":"0110011",
        "slt":"0110011",
         "sra":"0110011",
          "srl":"0110011",
           "sub":"0110011",
           "xor":"0110011",
            "mul":"0110011",
             "div":"0110011",
              "rem":"0110011"
        }
