import numpy as np

class RandomNumberGenerator:
    """
    A class that implements a random number generator using the Linear Congruential Generator (LCG) algorithm.

    Attributes:
        modulus (int): The modulus value for the LCG algorithm.
        multiplier (int): The multiplier value for the LCG algorithm.
        increment (int): The increment value for the LCG algorithm.
        startingVal (int): The starting value for the LCG algorithm.

    Methods:
        setModulus(modulus): Setter method for the modulus attribute.
        setMultiplier(multiplier): Setter method for the multiplier attribute.
        setIncrement(increment): Setter method for the increment attribute.
        setStartingVal(startingVal): Setter method for the startingVal attribute.
        generate(): Generates a random number using the LCG algorithm.

    """

    def __init__(self, modulus=2**31-1, multiplier=16807, increment=0, startingVal=None):
        """
        Initializes a RandomNumberGenerator object.

        Args:
            modulus (int): The modulus value for the LCG algorithm. Default is 2^31-1.
            multiplier (int): The multiplier value for the LCG algorithm. Default is 16807.
            increment (int): The increment value for the LCG algorithm. Default is 0.
            startingVal (int): The starting value for the LCG algorithm. If None, a random starting value is generated.

        """
        self.setModulus(modulus)
        self.setMultiplier(multiplier)
        self.setIncrement(increment)
        self.setStartingVal(startingVal)

    def setModulus(self, modulus):
        """
        Setter method for the modulus attribute.

        Args:
            modulus (int): The modulus value for the LCG algorithm.

        """
        self.__modulus = modulus

    def setMultiplier(self, multiplier):
        """
        Setter method for the multiplier attribute.

        Args:
            multiplier (int): The multiplier value for the LCG algorithm.

        """
        self.__multiplier = multiplier

    def setIncrement(self, increment):
        """
        Setter method for the increment attribute.

        Args:
            increment (int): The increment value for the LCG algorithm.

        """
        self.__increment = increment

    def setStartingVal(self, startingVal):
        """
        Setter method for the startingVal attribute.

        Args:
            startingVal (int): The starting value for the LCG algorithm. If None, a random starting value is generated.

        """
        if startingVal is None:
            startingVal = np.random.randint(0, self.__modulus)
        self.__startingVal = startingVal

    def __moduloSum(self, x, y, m):
        """
        Helper method to calculate the modulo sum of two numbers.

        Args:
            x (int): The first number.
            y (int): The second number.
            m (int): The modulus value.

        Returns:
            int: The modulo sum of x and y.

        """
        assert (x >= 0 and y >= 0), "0 ≤ x, y"
        assert (x <= m-1 and y <= m-1), "x, y ≤ m − 1"
        assert (type(x)==int)
        assert (type(y)==int)
        assert (type(m)==int)

        if (x <= m - 1 - y):
            return x + y
        else:
            return (x - (m - y)) % m

    def generate(self):
        """
        Generates a random number using the LCG algorithm.

        Returns:
            int: The generated random number.

        """
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
        self.setStartingVal(r)
        return r
