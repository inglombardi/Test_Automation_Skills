"""
Implement the class RealNumber and ComplexNumber to store a real and a complex number, respectively.
The first class has an attribute called "re" that stores the real part of a real number;

while the second class has two attributes, 're' and 'im' , to store the real and imaginary part
of a complex number, respectively.
Both classes have to implement the add() method, to sum up two numbers by calling n1.add(n2) , being
n1 and n2 any number (either real or complex).

Please use the double-dispatch design pattern
to avoid that the method n1.add(n2) checks the type of n2.

Implement a third class, named QuaternionNumber , whose instances
represent quaternions, namely, numbers represented by four coordinates  q = (a,b,c,d)
as: q = a + bi + cj + dk where i = sqrt(-1)

-Implement the method add() by accounting that:

(1) the sum of a real 'x' and a quaternion 'q' is given as :
    w = x + q = (x+a) + i(b) + j(c) + k(d)

(2) the sum of a complex number 'z' and a quaternion 'q' is given as :
    w = z + q = (x+iy) + (a + bi + cj + dk) = (x+a) + i(y+b) + j(c) + k(d)

(3) the sum of two quaternions 'q1' and 'q2' is given as :

    q1 = a + bi + cj + dk
    q2 = A + Bi + Cj + Dk
    w = q1 + q2 = [a+A] + [b+B]i + [c+C]j + [ d+D]k

different cases:
(1) real + real => real
(2) real + complex => complex
(3) real + quaternion => quaternion
(4) complex + complex => complex
(5) complex + quaternion => quaternion
(6) quaternion + quaternion => quaternion


"""
from abc import ABC, abstractmethod
from pyquaternion import Quaternion

class MathObject(ABC):
    def __str__(self):
        return self.__class__.__name__
    # --------- general method will dispatch second method for 2nd dispath
    # first dispatch
    @abstractmethod
    def add(self, otherNumber):
        pass # here there will be called the second method according to the local context

    # second dispatch : protected methods
    @abstractmethod
    def add_a_real(self, otherNum): # where self is a RealNumber
        pass

    @abstractmethod
    def add_a_complex(self, otherNum):  # where self is a ComplexNumber
        pass

    @abstractmethod
    def add_a_quaternion(self, otherNum):  # where self is a QuaternionNumber
        pass

class RealNumber(MathObject):
    def __init__(self, real_part=0):
        self._re = real_part

    # first dispatch
    def add(self, otherNum): # self => RealNumber
        """
        :param otherNum:
        (1) if otherNum is RealNumber => there will be called otherNum.add_a_real(self)
        (2) if otherNum is a ComplexNumber => there will be called otherNum.add_a_complex(self)
        (3) if otherNum is a QuaternionNumber => there will be called otherNum.add_a_quaternion(self)
        :return: result of operation
        """
        return otherNum.add_a_real(self)

    # second dispatch : protected methods
    def add_a_real(self, otherNum):  # where self is a RealNumber
        # here "self" is the previous otherNum
        """:param otherNum: it could be a real or complex or quaternion but it doesn't matter :
        only real part will be affected in any way """
        self._re += otherNum._re
        return self._re

    def add_a_complex(self, otherNum):  # where self is a ComplexNumber
        self._re += otherNum._re
        #self._im += otherNum._im # it must not be upgraded because otherNum is a real in this case
        z = complex(self._re, otherNum._im) # only to display it in a faster way and more clear way
        # the trick is to use otherNum._im because it's a complex and this trick avoid to use another attribute in a real
        # in fact a real number is a n=x+i0 thus it's more correct to avoid a null immaginary part in the init method
        # THIS TRICK IS VERY CLEVER instead of the solution in the " Exercise : Complex Number " in the pdf
        return z

    def add_a_quaternion(self, otherNum):  # where self is a QuaternionNumber
        self._re += otherNum._re
        # self._im += otherNum._im  it must not be upgraded because otherNum is a real in this case
        # self._jj = third_part  it must not be upgraded because otherNum is a real in this case
        # self._kk = fourth_part  it must not be upgraded because otherNum is a real in this case
        q = Quaternion(self._re, otherNum._im, otherNum._jj, otherNum._kk)
        return q

class ComplexNumber(MathObject):
    def __init__(self, real_part=0, immaginary_part=0):
        self._re = real_part
        self._im = immaginary_part

    # first dispatch
    def add(self, otherNum):  # self => ComplexNumber
        """
        :param otherNum:
        (1) if otherNum is RealNumber => there will be called otherNum.add_a_real(self)
        (2) if otherNum is a ComplexNumber => there will be called otherNum.add_a_complex(self)
        (3) if otherNum is a QuaternionNumber => there will be called otherNum.add_a_quaternion(self)
        :return: result of operation
        """
        return otherNum.add_a_complex(self)

    # second dispatch : protected methods
    def add_a_real(self, otherNum):  # where self is a RealNumber ( previous otherNum )
        # here "self" is the previous otherNum
        """:param otherNum: it could be a real or complex or quaternion but it doesn't matter :
        only real part will be affected in any way thus self._im will be invariant ... """
        self._re += otherNum._re
        # self._im is UNCHANGEABLE
        #self._im = otherNum._im
        z = complex( self._re, self._im)
        return z

    def add_a_complex(self, otherNum):  # where self and otherNum are both Complex Numbers
        self._re += otherNum._re
        self._im += otherNum._im
        z = complex(self._re, self._im)  # only to display it in a faster way and more clear way
        return z

    def add_a_quaternion(self, otherNum):  # where self is a QuaternionNumber
        self._re += otherNum._re
        self._im += otherNum._im
        # self._jj = third_part  it must not be upgraded because otherNum is a complex in this case z= x+iy + 0j +0k
        # self._kk = fourth_part  it must not be upgraded because otherNum is a complex in this case
        q = Quaternion(self._re, self._im, otherNum._jj, otherNum._kk)
        return q


class QuaternionNumber(MathObject):
    def __init__(self, real_part=0, immaginary_part=0, third_part=0, fourth_part=0):
        self._re = real_part
        self._im = immaginary_part
        self._jj = third_part
        self._kk = fourth_part

    # first dispatch
    def add(self, otherNum):  # self => QuaternionNumber
        """
        :param otherNum:
        (1) if otherNum is RealNumber => there will be called otherNum.add_a_real(self)
        (2) if otherNum is a ComplexNumber => there will be called otherNum.add_a_complex(self)
        (3) if otherNum is a QuaternionNumber => there will be called otherNum.add_a_quaternion(self)
        :return: result of operation
        """
        return otherNum.add_a_quaternion(self)

    # second dispatch : protected methods
    def add_a_real(self, otherNum):  # where self is a RealNumber ( previous otherNum )
        # here "self" is the previous otherNum
        """:param otherNum: it could be a real or complex or quaternion but it doesn't matter :
        only real part will be affected in any way thus self._im will be invariant ... """
        self._re += otherNum._re
        # self._im, self._jj and self._kk are UNCHANGEABLE
        q = Quaternion(self._re, self._im, self._jj, self._kk)
        return q

    def add_a_complex(self, otherNum):  # where self is a ComplexNumber and otherNum is a QuaternionNumber
        self._re += otherNum._re
        self._im += otherNum._im
        # self._jj and self._kk are UNCHANGEABLE because a complex z= x+iy + 0j +0k
        q = Quaternion(self._re, self._im, self._jj, self._kk)  # only to display it in a faster way and more clear way
        return q

    def add_a_quaternion(self, otherNum):  # where self and otherNum are both Quaternion Numbers
        self._re += otherNum._re
        self._im += otherNum._im
        self._jj += otherNum._jj
        self._kk += otherNum._kk
        q = Quaternion(self._re, self._im, self._jj, self._kk)
        return q


if __name__ == '__main__':
    print('-------- Quaternion class Test ----------')
    q = Quaternion([1., 0., 0., 0.])
    q.__dict__
    print(q)
    """
    1.000 +0.000i +0.000j +0.000k
    """

    print("--------------------------- solution with double dispatch approach ----------------------------------")
    list_of_numbers = [RealNumber(5), ComplexNumber(3, 2), QuaternionNumber(1,1,1,1)]
    r1 = RealNumber(1)
    r2 = RealNumber(1)
    z1 = ComplexNumber(1,1)
    z2 = ComplexNumber(1,1)
    q1 = QuaternionNumber(1,1,1,1)
    q2 = QuaternionNumber(1,1,1,1)

    print(" ------------ 1st test : real + real ")
    print(r1.__dict__)
    print(r2.__dict__)
    print(r1, '+', r2, '->', r1.add(r2))

    print(" ------------ 2nd.0 test :  complex + real")
    print(r1.__dict__)
    print(z1.__dict__)
    print(r1, '+', z1, '->', z1.add(r1))

    print(" ------------ 2nd.1 test : real + complex ")
    print(r1.__dict__)
    print(z1.__dict__)
    print(r1, '+', z1, '->', r1.add(z1))

    print(" ------------ 3rd test : complex + complex ")
    print(z1.__dict__)
    print(z2.__dict__)
    print(z1, '+', z2, '->', z1.add(z2))

    print(" ------------ 4th.0 test : complex + quaternion ")
    print(z1.__dict__)
    print(q1.__dict__)
    print(z1, '+', q1, '->', z1.add(q1))

    print(" ------------ 4th.1 test : quaternion + complex ")
    print(z1.__dict__)
    print(q1.__dict__)
    print(z1, '+', q1, '->', q1.add(z1))

    print(" ------------ 5th.0 test : quaternion + real ")
    r1 = RealNumber(1)
    q1 = QuaternionNumber(1, 1, 1, 1)
    print(r1.__dict__)
    print(q1.__dict__)
    print(r1, '+', q1, '->', r1.add(q1))

    print(" ------------ 5th.1 test : real + quaternion ")
    r1 = RealNumber(1)
    q1 = QuaternionNumber(1, 1, 1, 1)
    print(r1.__dict__)
    print(q1.__dict__)
    print(r1, '+', q1, '->', q1.add(r1))

    print(" ------------ 6th test : quaternion + quaternion ")
    print(q2.__dict__)
    print(q1.__dict__)
    print(q2, '+', q1, '->', q1.add(q2))

# ---------------------------------------------------------------------------------

"""
 Create a unittest class with a test to verify that w = q1 + z with
 quaternion q1 = 2+1i+2j+3k and z=5+2i is output with:
 w = 7+3i+2j+3k. 
 The quaternion q1 = 2+1i+2j+3k and z=5+2i ou and the
complex number should be instantiated in the setUp() method
"""

import unittest

class TestQuaternionAlgebra(unittest.TestCase):

    def setUp(self) -> None:
        self.q = QuaternionNumber(2,1,2,3)
        self.z = ComplexNumber(5,2)
        self.w = Quaternion(7,3,2,3)
    def test_add(self):
        self.assertEqual(self.q.add(self.z),self.w)

if __name__ == '__main__':
    """unittest.main() mette a disposizione un'interfaccia a riga di comando per testare lo script."""
    unittest.main()