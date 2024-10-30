#interface

class Customer:
    def __init__(self, strategy):
        self.cost = 0
        self.strategy = strategy

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