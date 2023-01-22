#initialize list of uid's
uid_List=[]
#load uid's that we would like a thickness for
with open('02a_uid_for_which_we_need_a_thickness.txt', 'r') as content:
    for line in content:
        x=line[:-1]
        uid_List.append(x)