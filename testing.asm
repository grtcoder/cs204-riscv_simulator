<<<<<<< HEAD
.data
var1 : .word 10,20,30,40,50
.text
addi x30,x0,1000
auipc x4,65536
addi x4,x4,-4
addi x5,x0,5
jal x6,sort
beq x0,x0,endprog


sort :

addi x20,x0,1
beq x5,x20,endddd
addi x7,x0,0
lw x8,0(x4)
addi x21,x0,0
loop :bge x7,x5,endloop 
addi x29,x0,2
sll x9,x7,x29
add x9,x4,x9
lw x9,0(x9)
bge x8,x9,else
addi x8,x9,0
addi x21,x7,0
else :
addi x7,x7,1
beq x0,x0,loop

endloop :
sll x21,x21,x29
add x22,x4,x21
lw x23,0(x4)
sw x23,0(x22)
sw x8,0(x4)

addi x30,x30,12 
sw x4,0(x30)
sw x5,4(x30)
sw x6,8(x30)
addi x4,x4,4
addi x5,x5,-1
jal x6,sort
lw x1,8(x30)
addi x30,x30,-12
jalr x0,x1,0
endddd :
jalr x0,x6,0


endprog :
=======
addi x0,x0,16
sw x16,0(x0)
lw x1,0(x0)
>>>>>>> c628ab8926caf9337fd689d40cd0800e3738b0ac
