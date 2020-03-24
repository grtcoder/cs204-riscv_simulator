import json
file=open('instruction_set.json','w+')
instructions =[['0']*32 for _ in range(32)]
#R format
#funct 7:

instructions[5][1]='1'
instructions[7][1]='1' 
instructions[9][6]='1' 
instructions[10][6]='1' 
instructions[11][6]='1' 

#funct 3:    
for j in range(17,20):
    for i in  range(0,12):
        if(j==17):
            if(i==1 or i==2 or i==5 or i==6 or i==8 or i==10 or i==11):
                instructions[i][j]='1'
        elif(j==18):
            if(i==1 or i==2 or i==4 or i==11):
                instructions[i][j]='1'
        else:
            if(i==1 or i==3 or i==5 or i==6):
                instructions[i][j]='1'

#opcodes:

for j in range(25,32):
    for i in range(12):
        if(j==25 or j==28 or j==29):
            instructions[i][j]='0'
        else:
            instructions[i][j]='1'


#for I and S format funct 3 
for j in range(17,20):
    for i in range(12,24):
        if(j==19 and (i==13 or i==16 or i==17 or i==22 or i==23)):
            instructions[i][j] ='1'
        elif(j==18 and (i==13 or i==14 or i==16 or i==18 or i==21 or i==22)):
            instructions[i][j]='1'
        elif (j==17 and (i==13 or i==14)):
            instructions[i][j]='1'
        else: 
            instructions[i][j]='0'
# for i and s format opcode

for j in range(25,32):
    for i in range(12,24):
        if(j==30 or j==31):
            instructions[i][j]='1'
        elif (j==29 and i==19):
            instructions[i][j]='1'
        elif (j==27 and (i==12 or i==13 or i==14)):
            instructions[i][j]='1'
        elif (j==26 and (i==19 or i==20 or i==21 or i==22 or i==23)):
            instructions[i][j]='1'
        elif (j==25 and (i==19)):
            instructions[i][j]='1'
        else :
            instructions[i][j]='0'
            
#opcode for last 7 instructions

for j in range(25,32):
    for i in  range(24,28):
        if (j==25 or j==26 or j==30 or j==31):
            instructions[i][j]='1'
        else:
            instructions[i][j]='0'
        if(j==25 or j==26 or j==28):#for auipc
            instructions[28][j]='0'
        else:
            instructions[28][j]='1'
        if(j==25 or j==28):#for lui
            instructions[29][j]='0'
        else:
            instructions[29][j]='1'
        if(j==27):#for jal
            instructions[30][j]='0'
        else:
            instructions[30][j]='1'

#funct3
for j in range(17,20):
    for i in range(24,28):
        if(j==17 and (i==24 or i==25)):
            instructions[i][j]='0'
        elif(j==17 and (i==26 or i==27)):
            instructions[i][j]='1'
        elif(j==18):
            instructions[i][j]='0'
        elif(j==19 and (i==24 or i==26)):
            instructions[i][j]='0'
        else:
            instructions[i][j]='1'

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
    "beq":instructions[24],
    "bne":instructions[25],
    "bge":instructions[26],
    "blt":instructions[27],
    "auipc":instructions[28],
    "lui":instructions[29],
    "jal":instructions[30],
}
temp=json.dumps(opcodes)
file.write(temp)
file.close()
