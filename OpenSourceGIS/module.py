def num_higher_(s,s_high):
    num=0
    for a in s:
        if a >= s_high:
            num = num+1
    return num

def num_lower_(s,s_low):
    num=0
    for a in s:
        if a < s_low:
            num = num+1
    return num