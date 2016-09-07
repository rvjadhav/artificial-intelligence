from __future__ import division
import numpy as np
import math
def expo(x):
    ans,newAns,count = 1,1,1
    prevTerm = x
    while (math.fabs(prevTerm) > 0.00001):
        ans = ans + prevTerm
        count += 1
        prevTerm *= x/count
        newAns = ans + prevTerm
    return newAns

if __name__ == '__main__':
    positive = [];
    negative = [];
    positive.append(np.exp(1)-expo(1))
    positive.append(np.exp(5)-expo(5))
    positive.append(np.exp(10)-expo(10))
    positive.append(np.exp(15)-expo(15))
    positive.append(np.exp(20)-expo(20))
    negative.append(np.exp(-1)-expo(-1))
    negative.append(np.exp(-5)-expo(-5))
    negative.append(np.exp(-10)-expo(-10))
    negative.append(np.exp(-15)-expo(-15))
    negative.append(np.exp(-20)-expo(-20))
    print (positive)
    print (negative)