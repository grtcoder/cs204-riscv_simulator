#control signals pc_select, pc_enable, inc_select are assumed to be given and ra and imm are in binary
#if ra and imm are not in binary, we need to make a function to convert them into binary
#all values are represented as binary strings
# curr program counter is either passed or stored as a global variable(binary string)

def to_binary(a):
    s = ""
    while (a):
        s += str(a%2)
        a = a//2
    return ("".join(reversed(s)))

def to_decimal(a):
    return int(a,base=2)

def iag(pc_select, pc_enable, inc_select, imm, ra,curr_pc):#pass line difference in imm field
    temp_pc = ""
    mux_inc = 4
    mux_pc = 0
    if(pc_select == 0):
        temp_pc = ra
    else:
        temp_pc = curr_pc
    if(pc_enable == 1):
        if(inc_select == 0):
            mux_inc = 4
        else:
            mux_inc = to_decimal(imm)
        mux_pc = to_decimal(temp_pc) + mux_inc
        mux_pc = to_binary(mux_pc)
        # returns mux_pc for mux y
        return mux_pc
