import os
if(1):
    Knob1 = int(input("Do you want to run pipelined(0) or non-pipelined version(1)?"))
    if(Knob1==1):
        os.system('python Phase3.py')
    else:
        Knob2 = int(input("Do you want Data Forwarding(0) or Data Stalling(1) to resolve dependencies?"))
        if(Knob2==0):
            os.system('python pipelined/Buff_Regs.py')
        elif(Knob2==1):
            os.system('python pipelined/Stalling.py')
        