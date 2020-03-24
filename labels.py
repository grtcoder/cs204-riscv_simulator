# import sys
# filename=sys.argv[1]#commands like python <file_name> (<risc-v code path>) => sys.argv[1]
# if(not filename.endswith('.asm')):
#     print("This file format is invalid")
#     sys.exit()
# f=open(filename,'r+')
# lines=f.read().splitlines()
def labelize(lines):
    ct = 0
    dict = {}
    for i in lines:
        ln = len(i)
        lbl = ""
        flag = 0
        fflag = 1
        for j in range(ln):
            if i[j] == ':':
                flag = 1
                if j == ln -1:
                    fflag = 0
                break
            lbl += i[j]
        if flag == 1:
            dict[lbl.strip()] = ct
        if fflag == 1:
            ct += 4
    return dict
