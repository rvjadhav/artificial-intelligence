# refer www.strchr.com/standard_deviation_in_one_pass
# to confirm answers www.easycalculation.com/statistics/standard-deviation.php
from __future__ import division
import math
import numpy
def tp(sequence):
    sum = 0
    mean = numpy.mean(sequence)
    for x in sequence:
        sum = sum + math.pow(x-mean,2)
    ans = math.sqrt(sum/(len(sequence)-1))
    return ans

def op(sequence):
    sqrSum = 0
    meanSqr = math.pow(numpy.mean(sequence),2)
    for x in sequence:
        sqrSum = sqrSum + math.pow(x,2)
    ans = math.sqrt(sqrSum / (len(sequence)-1) - meanSqr)
    return ans

if __name__ == '__main__':
    sequence = [1,2,3,4,5,6,7,8,9,10]
    bad_sequence = [100,1,3000,2,50000,3,27000,800,1,100000]
    #Any squence with large numbers is a bad_sequence
    var_seq_tp = tp(sequence)
    print ("Two pass: %f"%var_seq_tp)
    var_seq_op = op(sequence)
    print ("One pass: %f"%var_seq_op)
    bad_var_seq_tp = tp(bad_sequence)
    print ("Two pass: %f"%bad_var_seq_tp)
    bad_var_seq_op = op(bad_sequence)
    print ("One pass: %f"%bad_var_seq_op)