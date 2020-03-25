CS204 RISC-V Simulator Phase 1 and Phase 2

Group:

Adarsh Kumar     -2018CSB1066

Akshay Gahlot    -2018CSB1068

Ankit Bhadu      -2018CSB1073

Divyanshu Mathpal-2018CSB1086

G Pradyumn       -2018CSB1088

instruction to run 
GUI- first do pip freeze > requirements.txt
then python final_1.py
PS:-
->code should not contain comments
->Labels cannot be of the form label:. ':' should be separated by space from label name
->Arguments of instructions should be comma separated 
->do not use pseudonames of registers, Address them as x0,x1,........,x10,....,x15,......,x29,.....,x31.
dont use pseudonames like stack pointer

size of memory is 100000 bits

data starts   2016

The compiler is bit addressable. Regular riscv code will have to be modified (such as offset provided and addition to stack pointer. An example code for recursive bubble sort is given for the reference) to run the code.


Contributions:


Instruction Set-Adarsh,Ankit,Divyanshu,Pradyumn

ALU-Adarsh,Akshay

Memory and Register Read Write-Adarsh,Akshay

Machine code generation- ankit

Handling of Labels-Ankit,Akshay,Adarsh

Error handling- Ankit, Divyanshu

GUI-Divyanshu 

IAG-Pradyumn


Sample code -

.data

var1 : .word 10,9,56,90,10

.text

addi x30,x0,1000

addi x4,x0,2016

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

addi x29,x0,5

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



addi x30,x30,96 

sw x4,0(x30)

sw x5,32(x30)

sw x6,64(x30)

addi x4,x4,32

addi x5,x5,-1

jal x6,sort

lw x1,64(x30)

addi x30,x30,-96

jalr x0,x1,0

endddd :

jalr x0,x6,0


endprog :
