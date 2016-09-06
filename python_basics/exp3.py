from __future__ import division
import numpy as np
def expo(x):
    if x<0:
        a=-x
    err,ans,newAns,count = 1,1,1,1
    prevTerm = a
    while (err>0.00001):
        ans = ans + prevTerm
        count += 1
        prevTerm *= a/count
        newAns = ans + prevTerm
        err = newAns - ans
    if x<0:
        newAns=1/newAns
    return newAns

if __name__ == '__main__':
    negative = [];
    negative.append(np.exp(-1)-expo(-1))
    negative.append(np.exp(-5)-expo(-5))
    negative.append(np.exp(-10)-expo(-10))
    negative.append(np.exp(-15)-expo(-15))
    negative.append(np.exp(-20)-expo(-20))
    print (negative)