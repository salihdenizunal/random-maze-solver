import numpy as np
import scipy.signal as sp
import matplotlib.pyplot as plt
import sys
from bisect import bisect_left
from itertools import permutations as perms

plt.rcParams['figure.figsize'] = [7.5, 7.5] # This is to adjust the image size on Jupyter

def modulosum(x, y, m):
    assert (x >= 0 and y >= 0), "0 ≤ x, y"
    assert (x <= m-1 and y <= m-1), "x, y ≤ m − 1"
    assert (type(x)==int)
    assert (type(y)==int)
    assert (type(m)==int)

    if (x <= m - 1 - y):
        return x + y
    else:
        return (x - (m - y)) % m

def lcgrandom(fun=lcg2, modulus=2**32-1, multiplier=367, increment=314, initval=1, num=1):
    # Check conditions
    assert(fun==lcg2), "This function can only be used with lcg2 function."
    randlist = []; # Create an empty list to populate
    for ind in range(num):
        val = fun(modulus, multiplier, increment, initval)
        initval = val # Set the previous random number as the new seed
        randlist.append(val) # Append to the list
    return np.array(randlist)

def spectraltest(modulus=256, multiplier=21, increment=11, startingval=0, num=512, t=2):
    randlist = lcgrandom(lcg2, modulus, multiplier, increment, startingval, num)
    x = randlist[0::2]
    y = randlist[1::2]
    plt.plot(x, y, 'b.')
    plt.axis('square')
    plt.axis('tight')
    plt.show()
    return 0

# Second LCG implementation in the book (p.21 in the 2017 edition)
def lcg2(modulus=2**31-1, multiplier=16807, increment=0, startingval=1):
    # Check inputs if they are valid.
    assert (modulus >= 1), "Modulus should be greater than or equal to 1. (1 ≤ m)"
    assert (multiplier >= 0 and multiplier <= modulus - 1), "Multiplier should be greater or equal\
to 0 and should be smaller than or equal to modulus - 1. (0 ≤ a ≤ m − 1)"
    assert (increment >= 0 and increment <= modulus - 1), "Incrementshould be greater or equal to\
0 and should be smaller than or equal to modulus - 1. (0 ≤ c ≤ m − 1)"
    assert (startingval >= 0 and startingval <= modulus - 1), "Starting should be greater or equal\
to 0 and should be smaller than or equal to modulus - 1. (0 ≤ X0 ≤ m − 1)"
    assert ((modulus % multiplier) <= np.floor(modulus / multiplier)), "(m mod a) ≤ floor(m / a)"

    # LCG algorithm.
    q = modulus // multiplier
    p = modulus % multiplier
    r = multiplier * (startingval % q) - p * (startingval // q)
    if r < 0:
        r = r + modulus
    r = modulosum(r, increment, modulus)
    return r