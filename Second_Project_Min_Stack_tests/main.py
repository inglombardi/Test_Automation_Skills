"""
==============================
  DOCUMENTATION ABOUT TASKS
==============================

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the MinStack class:

MinStack() initializes the stack object.
void push(int val) pushes the element val onto the stack.
void pop() removes the element on the top of the stack.
int top() gets the top element of the stack.
int getMin() retrieves the minimum element in the stack.
You must implement a solution with O(1) time complexity for each function.

Example 1:

Input
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

Output
[null,null,null,null,-3,null,0,-2]

Explanation
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); // return -3
minStack.pop();
minStack.top();    // return 0
minStack.getMin(); // return -2


Constraints:

-231 <= val <= 231 - 1
Methods pop, top and getMin operations will always be called on non-empty stacks.
At most 3 * 104 calls will be made to push, pop, top, and getMin.

==============================
DOCUMENTATION ABOUT BUILTINS
==============================
import inspect

def esempio():
    return inspect.currentframe().f_code.co_name

# Chiamata alla funzione
print(esempio())

"""

import datetime
import inspect
clock_string = f"[{datetime.datetime.now()}]"


def display_status_msg(string):
  print("**********************************************************************************************************************************************************************************")
  print(f"\t\t\t\t\t\t\t*****{string}*****")
  print("**********************************************************************************************************************************************************************************")


class MinStack:

    def __init__(self):
        """
        :param self: the local context
        :return: an instance of the class
        Layout of the stack_list :
        [ [-2], [0] , [-3] , [] ]
                             head = len(stack_list) - 1


        """
        # Dynamic Memory: the append adds a new item without memory allocation problem and the Garbage Collector is automatic
        self.stack_list = list()  # stack_list = []
        self.head = 0  # minimum acceaptable

    def push(self, val: int) -> None:
        """
        :param self: the local context
        :param val: an integer to place in the TOP (new item)
        :return: None
        """
        display_status_msg(string=clock_string + inspect.currentframe().f_code.co_name)
        self.stack_list.append(val)
        self.head += 1

    def pop(self) -> None:
        """
        :param self: the local context
        :param val: an integer to place on the TOP
        :return: None
        """
        display_status_msg(string=clock_string + inspect.currentframe().f_code.co_name)
        try:
            if self.head > 0:  # If at least 1 push has been done
                self.head -= 1
            else:
                raise ValueError(f"{clock_string} Error during pop: The head is {self.head}.")
        except Exception as e:
            print(e)

    def top(self) -> int:
        """
        :param self: the local context
        :return: an integer to placed on the TOP
        """
        display_status_msg(string=clock_string + inspect.currentframe().f_code.co_name)
        if self.head == 0:  # The head is 0 because no push has been done
            raise ValueError(f"{clock_string} Error during top: The head is {self.head}.")
            # return -1
        else:  # self.head > 0  If at least 1 push has been done
            return self.stack_list[self.head-1]  # self.stack_list[len(stack_list)-1]  or self.stack_list[self.head-1]

    def getMin(self) -> int:
        """
        This method has a solution with O(N) time complexity.
        The main problem in your code is that the getMin method modifies the stack during the operation, removing
        elements with pop() and not restoring them. As a result, the result is correct, but the stack is emptied in
        the process, which is not desirable.

        :param self: the local context
        :return: The minimum integer of the stack
        """
        display_status_msg(string=clock_string + inspect.currentframe().f_code.co_name)
        aux_min = self.top()
        while self.head != 0:
            self.pop()
            if self.head == 0:
                break
            temp = self.top()
            if temp < aux_min:
                aux_min = temp
        # here head == 0
        return aux_min

    @staticmethod
    def display_obj(obj_attr_dict: dict):
        """
        :param obj_attr_dict: obj.__dict__
        :return: None
        """
        display_status_msg(string=inspect.currentframe().f_code.co_name)
        for key, val in obj_attr_dict.items():
            print(f"{key} : {val}")


if __name__ == '__main__':
    # Your MinStack object will be instantiated and called as such:
    display_status_msg(string="STACK CREATION")
    obj = MinStack()
    MinStack.display_obj(obj_attr_dict=obj.__dict__)
    obj.push(val=3)
    param_3 = obj.top()
    obj.pop()
    item_to_add = [-2, 4, 45]
    item_to_add2= list(range(-5, 5, 2))
    obj.push(val=-2) # "-2" replaces "3"
    newList = item_to_add2+item_to_add
    for el in newList:
        obj.push(el)
    print("\n\n\n\n\n\n\n\n\n")
    MinStack.display_obj(obj_attr_dict=obj.__dict__)
    print("\n\n\n\n\n\n\n\n\n")
    print(f"{clock_string} Algorithm O(N) obj.getMin() -> found {obj.getMin()}")