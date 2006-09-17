import math
def t_add(a,b):
    return a[0]+b[0],a[1]+b[1]
def t_sub(a,b):
    return a[0]-b[0],a[1]-b[1]
def t_mul(a,b):
    return a[0]*b[0],a[1]*b[1]
def t_div(a,b):
    return int(a[0]/b[0]),int(a[1]/b[1])
def t_abs(a):
    return abs(a[0]),abs(a[1])

def within_sight(who,life):
    if who==life:
        return False
    temp = t_abs(t_sub(life.position,who.position))
    dist = (temp[0]+temp[1])/2
    #dist = math.sqrt(temp[0]**2+temp[1]**2)
    if dist<=who.sight:
        return True
    else:return False

if __name__=='__main__':
    print t_div((1000.234,1000.345),(512,256))
