from Memory_initializations import *     
from Readwrite import write_from_memory
def fetch(addr):
       instruction=write_from_memory(addr,4,reg_id)
       return instruction