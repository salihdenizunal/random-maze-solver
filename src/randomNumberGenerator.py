import numpy as np

class RandomNumberGenerator:
    def __init__(self, modulus=2**31-1, multiplier=16807, increment=0, startingVal=1):
        self.__modulus = modulus
        self.__multiplier = multiplier
        self.__increment = increment
        self.__startingVal = startingVal

    def __moduloSum(self, x, y, m):
        assert (x >= 0 and y >= 0), "0 ≤ x, y"
        assert (x <= m-1 and y <= m-1), "x, y ≤ m − 1"
        assert (type(x)==int)
        assert (type(y)==int)
        assert (type(m)==int)

        if (x <= m - 1 - y):
            return x + y
        else:
            return (x - (m - y)) % m

    # Second LCG implementation in the book (p.21 in the 2017 edition).
    def generate(self):
        # Check inputs if they are valid.
        assert (self.__modulus >= 1), "Modulus should be greater than or equal to 1. (1 ≤ m)"
        assert (self.__multiplier >= 0 and self.__multiplier <= self.__modulus - 1), "Multiplier should be greater or equal\
    to 0 and should be smaller than or equal to modulus - 1. (0 ≤ a ≤ m − 1)"
        assert (self.__increment >= 0 and self.__increment <= self.__modulus - 1), "Incrementshould be greater or equal to\
    0 and should be smaller than or equal to modulus - 1. (0 ≤ c ≤ m − 1)"
        assert (self.__startingVal >= 0 and self.__startingVal <= self.__modulus - 1), "Starting should be greater or equal\
    to 0 and should be smaller than or equal to modulus - 1. (0 ≤ X0 ≤ m − 1)"
        assert ((self.__modulus % self.__multiplier) <= np.floor(self.__modulus / self.__multiplier)), "(m mod a) ≤ floor(m / a)"

        # LCG algorithm.
        q = self.__modulus // self.__multiplier
        p = self.__modulus % self.__multiplier
        r = self.__multiplier * (self.__startingVal % q) - p * (self.__startingVal // q)
        if r < 0:
            r = r + self.__modulus
        r = self.__moduloSum(r, self.__increment, self.__modulus)
        return r