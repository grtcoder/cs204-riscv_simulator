# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 20:45:16 2020

@author: roronoa_
"""

from ALU import alu
from Read_write import RW

def split(s):
    return [char for char in s]

while 1 :
    x = input()
    x = split(x)
    # print(len(x))
    machine_code = []
    for i in range(32-len(x)):
        machine_code.append(int(0))
    print(len(machine_code))
    # print(machine_code)
    for i in range(len(x)):
        machine_code.append(int(x[i]))
    print(machine_code)
    aluVal = alu(machine_code)
    # print(aluVal)
    aluVal = split(aluVal)
    print(aluVal)
    RW(machine_code,aluVal,0)
    for i in range(3):
        for j in range(32):
            print (reg[i][j],end = " ")