# import sys
# filename=sys.argv[1]#commands like python <file_name> (<risc-v code path>) => sys.argv[1]
# if(not filename.endswith('.asm')):
#     print("This file format is invalid")
#     sys.exit()
# f=open(filename,'r+')
# lines=f.read().splitlines()
linetoPC = []
def labelize(lines):
    ct = 0
    dict = {}
    k = 0
    for i in lines:
        i=i.strip()
        ln = len(i)
        if(ln==0):
            continue
        lbl = ""
        flag = 0
        fflag = 1
        for j in range(ln):
            if i[j] == ':':
                flag = 1
                if j == ln -1:
                    fflag = 0
            if i[j]=='.':
                fflag=0
                break
            if(flag==0):    
                lbl += i[j]
        if flag == 1:
            dict[lbl.strip()] = ct
        linetoPC.append(ct)
#         k += 4
        if fflag == 1:
            ct += 4
    return dict
