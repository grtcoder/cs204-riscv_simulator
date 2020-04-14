from Memory_initializations import *
def fetch(addr):
       instruction=MEM[addr:addr+32]
       ######################## add pc updation herei
       return instruction