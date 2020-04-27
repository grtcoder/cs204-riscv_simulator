import sys
import json
import copy 
from bitstring import Bits
import labels as glabels
from labels import cmdtoPC
import os
from ALU_Phase3 import *

# filename=sys.argv[1]#commands like python <file_name> (<risc-v code path>) => sys.argv[1]
# if(not filename.endswith('.asm')):
#     print("This file format is invalid")
#     sys.exit()
# f=open(filename,'r+')
jfile=open("instruction_set.json","r+")
# lines=f.read().splitlines()
# terminate=False
# reg=[[0 for x in range(0,32)] for x in range(0,32)]
# MEM=[0 for x in range(0,100000)]
def firstoc(str,char):#for splitting command from the first space
    for i in range(len(str)):
        if str[i]==char:
            return i
    return -1
# label_dict=glabels.labelize(lines)
#print(label_dict)
tfile=open('type.json','r+')
type=json.load(tfile)
instruction_set=json.load(jfile)
def is_valid_reg(str1):
    for i in range(32):
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
def get_binimm3(str1,length1):
    num= int(str1)
    b = Bits(int=num, length=length1)
    # binary  = bin(int(num)).replace("0b", "")
    # while len(binary)<length1:
    #          binary = '0'+binary
    return b.bin  
def get_binimm(str1,length1):
    str1=str1.replace('x','')
    num= int(str1)
    b = Bits(int=num, length=length1)
    # binary  = bin(int(num)).replace("0b", "")
    # while len(binary)<length1:
    #          binary = '0'+binary
    return b.bin      
# def split(str):
#     return [char for char in str]
def machine_code(command,inputs,label_dict):    #typewise machine code generator
    # f=open('machine_code.mc','w+')
    code=[]
    for i in range(len(command)):#moving command by command
        command[i]=command[i].strip()
        if type[command[i]]=="R":
            # print(command[i])
            instruction=copy.deepcopy(instruction_set[command[i]])
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
                instruction[32-12:32-7]=get_bin(rd,5)
                instruction[7:12]=get_bin(rs2,5)
                instruction[12:17]=get_bin(rs1,5)
                # print(len(instruction))
                # print(instruction)
            
        elif type[command[i]]=="I":
            instruction=copy.deepcopy(instruction_set[command[i]])
            temp=inputs[i]
            # print(command[i])
            rs1=''
            rs2=''
            rd=''
            if len(temp) == 2 : # for stmts like ld lw etc
                rs1 = temp[1][temp[1].find("(")+1:temp[1].find(")")]
                imm = temp[1][0:temp[1].find("(")]
                rd= temp[0]
                instruction[32-12:32-7]=get_bin(rd,5)
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
                instruction[32-12:32-7]=get_bin(rd,5)
                instruction[0:12]=get_binimm(imm,12)
                instruction[12:17]=get_bin(rs1,5)
                # print(len(instruction))
                # print(instruction)
        elif type[command[i]]=="S":
            # print(command[i])
            instruction=copy.deepcopy(instruction_set[command[i]])
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
            # print(command[i])
            instruction=copy.deepcopy(instruction_set[command[i]])
            temp=inputs[i]
            rs1=''
            rs2=''
            rd=''
            if len(temp) == 3 : # for stmts like beq bge  etc
                rs1 = temp[0] 
                imm = label_dict[temp[2].strip()]#changed to accommodatr labels
                rs2= temp[1]
                imm=int(imm)-int(cmdtoPC[i])
                bina = get_binimm3(imm,13)
                # print(imm,bina)
                # print(instruction,"hohohohoh")
                instruction[0]= bina[0]
                instruction[24]=bina[1]
                instruction[1:7]   = bina[2:8]#for imm
                instruction[20:24] =bina[8:12]# for imm
                instruction[12:17] =get_bin(rs1,5)# for rs1
                instruction[7:12]  =get_bin(rs2,5)
                # print(len(instruction))
                #print(imm,bina)
                # print(instruction)
        elif type[command[i]]=="U":
            # print("U")
            # print(command[i])
            instruction=copy.deepcopy(instruction_set[command[i]])
            temp=inputs[i]
            if len(temp) == 2 and command[i]=='lui': # 
                rd = temp[0]
                imm = temp[1]
                bina = get_binimm3(imm,32)
                instruction[0:20]   =bina[12:32]#for imm(remember imm is reverses ie highest bit is 0)
                instruction[20:25] =get_bin(rd,5)# for rs1
                # print(len(instruction))
                # print(instruction)  
            elif len(temp) == 2 and command[i]=='auipc':
                rd = temp[0]
                imm = temp[1]
                imm=int(imm) 
                binaryi = get_binimm3(imm,32)
                bina=binaryi[12:32]
                bina=bina+'000000000000'
                # print(bina)
                txy=int(bina,2)
                txy=txy+int(cmdtoPC[i])
                bina=get_binimm3(txy,32)
                # print(bina)
                instruction[0:20]   =bina[0:20]#for imm(remember imm is reverses ie highest bit is 0)
                instruction[20:25] =get_bin(rd,5)
                # print(len(instruction))
                # print(instruction) 
        elif type[command[i]]=="UJ":
            # print("UJ")
            # print(command[i])
            instruction=copy.deepcopy(instruction_set[command[i]])
            temp=inputs[i]
            if len(temp) == 2 : # for stmts like ld lw etc
                rd = temp[0]
                imm = label_dict[temp[1].strip()]#changed to accommodatr labels
                imm=int(imm)-int(cmdtoPC[i])
                bina = get_binimm3(imm,21)  
                # print(label_dict)
                # print(imm,bina)
                instruction[0] = bina[0]
                instruction[12:20]   =bina[1:9]#for imm(remember imm is reverses ie highest bit is 0)
                instruction[11]= bina[9]
                instruction[1:11]=bina[10:20]
                instruction[20:25] =get_bin(rd,5)# for rs1
                # print(len(instruction))
                # print(instruction) 
        # print(len(instruction))
        # print(instruction)
        xyz= copy.deepcopy(instruction)
        code.append(xyz)
        #print("code",code)
    return code
# MEM = [None]*10000000
def get_binimm2(str1,length1):#for use in directives
    num= int(str1)
    b = Bits(int=num, length=length1)
    # binary  = bin(int(num)).replace("0b", "")
    # while len(binary)<length1:
    #          binary = '0'+binary
    return b.bin      
def write_to_memory_word(start, len, imm):#used in directives part
    x=get_binimm2(imm,len)
    print("hi",start,"  ",len,imm )
    
    for i in range(len//8):
        
        for j in range (8):
            MEM[j+start] = x[len-(i+1)*8+j]
        
        start =start+8
    #print(MEM[:i+start+1])
#comment this when merging
##note that there should be space after label name for this to work
def split_lines(lines,label_dict):
    commands=[]
    inputs=[]
    Current_data_inputs=0#offset from 1024 to start writing .data wala data\ 
    Start_data_dir=2016
    instruction_flag=1
    PC=0
    for i in range(len(lines)):
            xyz= lines[i].strip()
            if xyz=='':
                continue
            v=firstoc(lines[i],' ')
            command,inp=lines[i][:v],lines[i][v+1:]
            if command not in instruction_set.keys():#check if its a label or direcive and also  "continue" if executed a directive
                if command[-1]==':' or inp[0]==':' or command[0]=='.':#meaning its a label #last or condition to accomodate cases with directives but no label
                    in_arg= lines[i].split(':')
                    wxy='  '
                    if len(in_arg)==2:
                        wxy=in_arg[1].strip()
                    if wxy=='' and command[0]!='.':#this line only has label so do notheing
                        print ('encountered line with just label')
                        #todo call on rest instruction
                    elif len(in_arg)==2 or command[0]=='.':#2nd or condition is to accomodate cases with directives but no label
                        if len(in_arg)==2:
                            inst= in_arg[1].strip()
                        if command[0]=='.':# to accomodate cases with directives but no label
                            inst=lines[i].strip()
                        if inst[0]=='.':#its a directive
                            label_flag=1
                            label_dir=in_arg[0].strip()
                            if(label_dir[0]=='.'):
                                label_flag=0
                            u=firstoc(inst,' ')
                            ass_directive,dir_inp=inst[1:u],inst[u+1:]
                            if ass_directive=='data':
                                #print('got data directive')
                                instruction_flag=0
                            elif ass_directive=='text':
                                instruction_flag=1
                            elif ass_directive=='word':
                                words= dir_inp.split(',')
                                if(label_flag):
                                    label_dict[label_dir]= Start_data_dir + Current_data_inputs
                                    print(label_dict,label_dir)
                                for i in range(len(words)):
                                    write_to_memory_word(Start_data_dir+Current_data_inputs,32,words[i])
                                    Current_data_inputs=Current_data_inputs+32
                            elif ass_directive=='byte':
                                words= dir_inp.split(',')
                                if(label_flag):
                                    label_dict[label_dir]= Start_data_dir + Current_data_inputs
                                    #print(label_dict,label_dir)                            
                                for i in range(len(words)):
                                    write_to_memory_word(Start_data_dir+Current_data_inputs,8,words[i])
                                    Current_data_inputs=Current_data_inputs+8
                            elif ass_directive=='half':
                                words= dir_inp.split(',')
                                if(label_flag):
                                    label_dict[label_dir]= Start_data_dir + Current_data_inputs
                                    #print(label_dict,label_dir)
                                for i in range(len(words)):
                                    write_to_memory_word(Start_data_dir+Current_data_inputs,16,words[i])
                                    Current_data_inputs=Current_data_inputs+16
                            elif ass_directive=='dword':
                                words= dir_inp.split(',')
                                if(label_flag):
                                    label_dict[label_dir]= Start_data_dir + Current_data_inputs
                                    #print(label_dict,label_dir)
                                for i in range(len(words)):
                                    write_to_memory_word(Start_data_dir+Current_data_inputs,64,words[i])
                                    Current_data_inputs=Current_data_inputs+64
                            elif ass_directive=='asciiz':
                                words1= dir_inp.strip()

                                words=words1[1:len(words1)-1]
                                print('words ',words)
                                if(label_flag):
                                    label_dict[label_dir]= Start_data_dir + Current_data_inputs
                                    #print(label_dict,label_dir)
                                for i in range(len(words)):
                                    write_to_memory_word(Start_data_dir+Current_data_inputs,8,ord(words[i]))
                                    Current_data_inputs=Current_data_inputs+8
                        else:#just copy pasting below code coz its just a instruction with a label
                            inptemp=in_arg[1].strip()
                            v=firstoc(inptemp,' ')
                            command,input_argument=inptemp[:v],inptemp[v+1:]
                            input_arguments=input_argument.split(',')
                            commands.append(command)
                            for x in range(len(input_arguments)):
                                input_arguments[x]= input_arguments[x].strip()
                            inputs.append(input_arguments)
                    continue                  
                    # print("Unknown keyword",command)
                    # sys.exit()
            if instruction_flag==0:
                continue
            input_arguments=inp.split(',')
            # if(len(input_arguments)>3):
            #     print('Too many Arguments')
            #     sys.exit()
            commands.append(command)
            for x in range(len(input_arguments)):
                input_arguments[x]= input_arguments[x].strip()
            inputs.append(input_arguments)
            # print(input_arguments)
    return commands,inputs
def generate_machine_code(lines):
    label_dict=glabels.labelize(lines)
    commands,inputs=split_lines(lines,label_dict)
    print(label_dict)
    return machine_code(commands,inputs,label_dict),commands,inputs
# f.close()
def mc_gen(lines):
    y,p,q=generate_machine_code(lines)
    #print(y)
    z=[]
    for i in range(len(y)):
        yy=""
        for j in range(32): 
            yy+=y[i][j]
        # print(y,"this is y")
        v=hex(int(yy,2))
        z.append(v)
    return '\n'.join(z)
