""""
“Define a family of algorithms, encapsulate each one, and make them interchangeable. 
Strategy lets the algorithm vary independently from clients that use it” 
[Gamma, Erich, et al. "Elements of reusable object-oriented software.", 1995.]

Example
Write a program that manages drink orders in a pub. 

-Each customer can order one or more drinks declaring, in his add_drink() method, the number of drinks and the unit cost. 
-The total cost of the various orders is stored in a customer attribute. 
customer1.add_drink(1, 7) # 1 drink, 7 euros for each drink 
During the Happy Hour the customer declares the same price, but the drink is discounted by 50%. 
customer1.add_drink(1, 7) # it pays 3.5 euros

Moreover, the type of clothing will be appropriate for the situation. 
The get_actual_dress() method will print normal dress or happy hour dress, depending on the time.


"""""
import strategy

""""     __________________OPTIONAL_______________
HappyHour = 1 = True ==> discounted if and only if actualDress is 1=True

       A=HappyHour          B = actualDress        Y = A AND B
___________________ | _________________________ |  ________
        0           |           0               |   0
        0           |           1               |   0
        1           |           0               |   0
        1           |           1               |   1   
        
        Questi vincoli sono stati aggiunti solo per aumentare la difficoltà ai fini di implementare uno switch-case
"""
from customer import Customer
#from strategy import  #functions, not objects
#from strategy import

# classic approach will be showed to start improvement through "Strategy pattern"
# ---------------- FIRST SOLUTION: CLASSIC APPROACH -----------------------

class Customer1():

    """ the evening begins that the drink rate is standard and at midnight the Happy Hour starts for one hour """
    #declaring "happy_hour" as attribute I gain less attribute to pass as argument in add_drink

    def __init__(self):
        self._totalCost=0
        self._actualDress=False # False=0=normal    True=1=happy_Hour_dress
        self._HappyHour = False  # for example

        # toString Java method (equivalent)  ==> OPTIONAL
    def __str__(self):  # override in a Object Class method that will be in each child class with this definition
        return str(self.__class__.__name__)+ " total_orders_cost_Summary:" + str(self._totalCost) + " \n" + "Actual worn dress: " + str(self._actualDress) + "\n" + "Now is Happy Hour?" + str(self._HappyHour)

    # GETTER METHOD   OPTIONAL
    @property
    def totalCost(self):
        return self._totalCost

    # SETTER METHOD    OPTIONAL
    @totalCost.setter
    def totalCost(self, value):
        self._totalCost=value
    # GETTER METHOD

    def actualDress(self): #get_actual_dress()
        return self._actualDress

    # FALSE SETTER METHOD

    def actualDress(self): #change dress
        self._actualDress = not self._actualDress #ONE COMPLEMENT
        #self._actualDress=True

    def startHappyHour(self):
        self._HappyHour = True


    def validDiscount(self):    # OPTIONAL ==> to make "add_drinks()" as Single Responsible Principle
        if self.HappyHour == True and self._actualDress == True:
            return True
        else:
            return False


    def add_drink(self, n_drinks, price_for_each_drink):
        """
         A=HappyHour          B = actualDress        Y = A AND B
___________________ | _________________________ |  ________
        0           |           0               |   0          case#2 elif
        0           |           1               |   0          case#4 else
        1           |           0               |   0          case#3 elif
        1           |           1               |   1          case #1 if

        """
        # CASEs
        if self._HappyHour == True and self._actualDress == True:
            self._totalCost = self._totalCost + n_drinks * price_for_each_drink * 0.5  # discounted by 50%
        elif self._HappyHour == False and self._actualDress == False:
            self._totalCost = self._totalCost + n_drinks*price_for_each_drink # FULL PRICE
            #customer1.add_drink(2, 7) ==> self._totalCost + 2*7
        elif self._HappyHour == False and self._actualDress == True:
            self._totalCost = self._totalCost + n_drinks * price_for_each_drink #FULL PRICE
        else:
            self._totalCost = self._totalCost + n_drinks * price_for_each_drink  #FULL PRICE

#===============> DO NOT SCALABLE
#===============> Potentially complicated, nested conditional logic with k branch in n different modules.
#===============>Risk of introducing a maintenance challenge.

# Here it's visible a different behaviour according to the attribute value Happy Hour (merely losing Actual Address because optional)
# This method could be divided into different methods according to the strategy used

# # ---------------- FIRST SOLUTION: CLASSIC APPROACH but with optimization -----------------------

class PubCustomer():
    def __init__(self):
        self.bill=0

    # variable BEHAVIOUR
    def add_drink(self, n_drinks, price, happy_hour=False):
        if happy_hour:
            self.bill+=n_drinks*price*0.5
        else:
            self.bill+=n_drinks*price

    # variable BEHAVIOUR
    @staticmethod
    def get_actual_dress(happy_hour=False):
        if happy_hour:
            print("happy hour dress")
        else:
            print("normal dress")

    def print_bill(self):
        print(self.bill)

#with this smaller code the Client must know the "happy hour" parameter
#===============> DO NOT SCALABLE
#===============> Potentially complicated, nested conditional logic with k branch in n different modules.
#===============>Risk of introducing a maintenance challenge.

#------------------------ SECOND SOLUTION : ABSTRACT CLASS -----------------------

from abc import ABC, abstractmethod

class Customer(ABC):

	def __init__(self):
		self.cost = 0

	def print_bill(self):
		print(self.cost)

	@abstractmethod
	def add_drink(self, n, unit_cost):
		self.cost += n * unit_cost

	@staticmethod
	@abstractmethod
	def get_actual_dress():
		pass


class CustomerNormalHour (Customer):


    def add_drink(self, n, unit_cost):
    	super().add_drink(n,unit_cost )


    @staticmethod
    def get_actual_dress():
        print('normal dress')


class CustomerHappyHour(Customer):
	def add_drink(self, n, unit_cost):
		discount = 0.5
		super().add_drink(n,unit_cost *discount )
		#self.cost += discount * (n * unit_cost)

	@staticmethod
	def get_actual_dress():
		print('happy hour dress')








# ------------------------------------------------ THIRD SOLUTION: STRATEGY PATTERN APPROACH -----------------------

# why could I use strategy pattern? Because this simple example could grow in a more difficult series of different cases
# with a long "if-elif-else" structure

#------------------------------ in file strategy.py ------------------
# strategy#1 => normal
# strategy#2 => happyhour
#-------------------------- in file customer.py-----------------------
# interface => concrete stategy that selects a particular strategy at runtime

#HERE THERE IS A NOT MODULAR VERSION:



class CustomerI:
    def __init__(self, strategy):
        self.cost = 0
        self.strategy = strategy #this attribute will be used to change the local strategy in the main

    #def add_drink(self,):
    #    self._strategy.add_drink

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter                     #                     <---->
    def strategy(self, strategy):        # switch of strategy   _°\_
        self._strategy = strategy


#------------------- three fundamental methods --------------
    def print_bill(self):
        print(self.cost)

    def add_drink(self, n, unit_cost): # it depends on chosen Strategy
        self.cost += self.strategy.compute_price(n * unit_cost)

    def get_actual_dress(self): # it depends on chosen Strategy
        self.strategy.get_actual_dress()

# -------------------------------------------------------------------- END CLASS CUSTOMER ----

from abc import ABC, abstractmethod


class Strategy(ABC):

    # two methods that will change your behaviour
    # (1)
    @abstractmethod
    def compute_price(self, value):
        pass
    # (2)
    @abstractmethod
    def get_actual_dress(self):
        pass


class NormalStrategy(Strategy):  # normal behaviour
    def compute_price(self, value):
        return value

    def get_actual_dress(self):
        print('normal dress')


class HappyHourStrategy(Strategy):  # happy hour behaviour
    def compute_price(self, value):
        discount = 0.5  # 50%  => avoid magic number
        return value * discount

    def get_actual_dress(self):
        print('happy hour dress')


#--------------------------------------------------------------





if __name__ == '__main__':
    print("# ---------------- FIRST SOLUTION: CLASSIC APPROACH -----------------------")
    c1=Customer1(); #totalCost=0 , actualDress=False, HappyHour=False
    c1.add_drink(4,7) #28
    print(c1.__str__())
    print("------------")
    c1.startHappyHour()
    c1.add_drink(1,7) #35
    print(c1.__str__())
    print("------------")
    print(c1.actualDress())
    c1.add_drink(1, 7)  # 35+3.5
    print(c1.__str__())
    print("------------")

    print("# ---------------- FIRST SOLUTION: CLASSIC APPROACH with a smaller code-----------------------")
    c2=PubCustomer()
    c2.add_drink(1,7)
    c2.get_actual_dress()
    print("start happy hour")
    c2.add_drink(2,5,happy_hour=True)
    #static method could be used directly on class
    PubCustomer.get_actual_dress(happy_hour=True) #c2.get_actual_dress(happy_hour=True)

    c2.print_bill()

    print("# ---------------- SECOND SOLUTION: ABSTRACT CLASS -----------------------")
    # NORMAL BILLING
    customer1 = CustomerNormalHour()
    customer1.add_drink(1, 7)
    customer1.get_actual_dress()

    # START HAPPY HOUR (50% discount)
    customer1.__class__ = CustomerHappyHour
    # You are changing class at runtime.
    # It is possible, but are we sure it is a good idea?

    customer1.add_drink(2, 5)
    customer1.get_actual_dress()

    # FINAL BILL
    customer1.get_actual_dress()
    customer1.print_bill()  # 12

    print("---------------- THIRD SOLUTION: STRATEGY PATTERN APPROACH -----------------------")

    # the client must declare two strategy object
    normal_strategy=NormalStrategy()
    happy_hour_strategy=HappyHourStrategy()

    customer11=CustomerI(normal_strategy)
    customer11.add_drink(1,7)
    customer11.get_actual_dress()
    print("start happy hour ")
    customer11.strategy=happy_hour_strategy #change the strategy


    customer22=CustomerI(happy_hour_strategy)
    customer22.add_drink(1,7)
    customer11.get_actual_dress()