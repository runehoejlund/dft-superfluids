#load material thicknesses
#initialize list of uid's
uid_List_Sahar=[]
d_List_Sahar=[]
#load uid's that we would like a thickness for
with open('thicknesses_Sahar.txt', 'r') as content:
    for line in content:
        #x=line[:-1]
        currentline = line.split(",")
        uid=currentline[0]
        uid_List_Sahar.append(uid)
        thickness=currentline[2]
        thick_number=thickness.split(": ")
        d=thick_number[1][:-1]
        d_List_Sahar.append(float(d))
        #print(uid)
        #print(currentline[2][:-1])
        #print(d)
print(uid_List_Sahar)
print(d_List_Sahar)
print(len(uid_List_Sahar))