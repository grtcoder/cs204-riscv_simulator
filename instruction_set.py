import json
file=open('instruction_set.json','w+')
instructions =[[0]*32 for _ in range(32)]

#fucnt 7:

instructions[5][1]=1
instructions[7][1]=1 
instructions[9][6]=1 
instructions[10][6]=1 
instructions[11][6]=1 

#funct 3:    

#opcodes:

for j in range(25,32):
    for i in range(12):
        if(j==25 or j==28 or j==29):
            instructions[i][j]=0
        else:
            instructions[i][j]=1


#for I and S format funct 3 
for j in range(12,15):
    for i in range(12,24):
        if(j==12 and (i==13 or i==16 or i==17 or i==22 or i==23)):
            instructions[i][j] = 1
        elif(j==13 and (i==13 or i==14 or i==16 or i==18 or i==21 or i==22)):
            instructions[i][j]=1
        elif (j==14 and (i==13 or i==14)):
            instructions[i][j]=1
        else: 
            instructions[i][j]=0
# for i and s format opcode

for j in range(0,7):
    for i in range(12,24):
        if(j==0 or j==1):
            instructions[i][j]=1
        elif (j==2 and i==19):
            instructions[i][j]=1
        elif (j==4 and (i==12 or i==13 or i==14)):
            instructions[i][j]=1
        elif (j==5 and (i==19 or i==20 or i==21 or i==22 or i==23)):
            instructions[i][j]=1
        elif (j==6 and (i==19)):
            instructions[i][j]=1
        else :
            instructions[i][j]=0 
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
    "rem":instructions[11],
    "addi":instructions[12],
    "andi":instructions[13], 
    "ori":instructions[14], 
    "lb":instructions[15],
    "ld":instructions[16], 
    "lh":instructions[17],
    "lw":instructions[18],
    "jalr":instructions[19],
    "sb":instructions[20],
    "sw":instructions[21], 
    "sd":instructions[22],
    "sh":instructions[23],
}
temp=json.dumps(opcodes)
file.write(temp)
file.close()