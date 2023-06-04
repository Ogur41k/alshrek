def get_digit(s:str):
    d= False
    t = []
    for i in s:
        if i.isdigit():
            t.append(i)
            d = True
        elif d:
            return ''.join(t)
    return ''.join(t)
def clean(s:list,e):
    while s.count(e)!=0:
        s.remove(e)
    return s
def russian(s:str):
    try:
        s= s.split('упр.')[1].strip().split(',')
        for i in range(len(s)):
            s[i] = get_digit(s[i].strip()) if get_digit(s[i].strip())!='' and int(get_digit(s[i].strip()))>10 else ''
        if int(s[0])>10:
            return clean(s,'')
        else:
            return []
    except:
        return []