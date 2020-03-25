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

def to_decimal(arr):
    sum=0
    for i in range(len(arr)):
        sum+=(int(arr[i]))*(2**(len(arr)-1-i))
    return sum

def to_list(s):
    return [char for char in s]

def iag(pc_select, pc_enable, inc_select, imm, ra,curr_pc):#line number to which we have to jump is passed in imm
    # print('got imm',imm)
    temp_pc = ""
    mux_inc = 4
    mux_pc = 0
    print("inc_select"+str(inc_select))
    ra = to_decimal(ra)
    if(pc_select == 0):
        temp_pc = ra//4
    else:
        temp_pc = curr_pc
    if(pc_enable == 1):
        if(inc_select == 0):
            mux_inc = 1
        else:
            # print('imm',imm)
            mux_inc = imm//4  
            # print('imm//4',mux_inc)
        mux_pc = temp_pc + mux_inc
        # print('mux pc',temp_pc,mux_inc,mux_pc)
        # returns mux_pc for mux y
        return mux_pc
