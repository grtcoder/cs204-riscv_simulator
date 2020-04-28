addi x10,x0,6
addi x2,x0,255
auipc x1,0
addi x0,x0,0
addi x1,x1,88
fact : addi x2,x2,-8 
sw x1,4(x2)
sw x10,0(x2)
addi x5,x10,-1
addi x7, x0, 1
bge x5,x7,L1
addi x10,x0,1
addi x2,x2,8
jalr x0,0(x1)
L1 : addi x10,x10,-1
jal x1,fact
addi x6,x10,0
lw x10,0(x2)
lw x1,4(x2)
addi x2,x2,8
mul x10,x10,x6
jalr x0,0(x1)
end : addi x1,x0,1
addi x0,x0,0
addi x0,x0,0
