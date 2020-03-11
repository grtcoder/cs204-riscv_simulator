
#control signals pc_select, pc_enable, inc_select are assumed to be given and ra and imm are in binary
#if ra and imm are not in binary, we need to make a function to convert them into binary
#all values are represented as binary strings

temp_pc = "0"

def iag(pc_select, pc_enable, inc_select, imm, ra, next_pc):
    mux_inc = "0"
    mux_pc = ""
    if(pc_select == 0):
        temp_pc = ra
    else:
        temp_pc = next_pc
    if(pc_enable == 1):
        if(inc_select == 0):
            mux_inc = "100"
        else:
            mux_inc = imm
        while(mux_inc.size()<temp_pc.size()):
            mux_inc = '0'+mux_inc
        while(temp_pc.size()<mux_inc.size()):
            temp_pc = '0'+temp_pc
        i = temp_pc.size()-1
        s = 0
        while(i>=0):
            a = temp_pc[i]-'0'
            b = mux_inc[i]-'0'
            mux_pc = '0' + (a^b^s)
            s = (a&b)|(b&s)|(a&s)
            i = i-1
        # returns temp_pc for mux y and next_pc which can be used to call this function again
        pc = [temp_pc, mux_pc]
        return pc