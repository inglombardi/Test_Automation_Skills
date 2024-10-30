from abc import ABC, abstractmethod

class Strategy(ABC):
    
    @abstractmethod
    def get_actual_price(self, value):
        pass
    @abstractmethod
    def get_actual_dress(self):
        pass






class NormalStrategy(Strategy): #normal behaviour
    def get_actual_price(self, value):
        return value

    def get_actual_dress(self):
        print('normal dress')


class HappyHourStrategy(Strategy): #happy hour behaviour
    def get_actual_price(self, value):
        discount=0.5 #50%
        return value*discount

    def get_actual_dress(self):
        print('happy hour dress')