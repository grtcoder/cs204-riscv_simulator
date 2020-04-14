.data
var1 : .asciiz "madem"
.text
addi x3,x0,2016
addi x6,x0,32
addi x9,x0,0
loop :

add x7,x3,x6
add x8,x3,x9
lb x4,0(x8)
lb x5,0(x7)
beq x9,x6,success
addi x9,x9,8
addi x6,x6,-8
beq x4,x5,loop
beq x0,x0,unsuccessful

success :
addi x1,x0,7
beq x0,x0,end
unsuccessful :
addi x1,x0,5

end :