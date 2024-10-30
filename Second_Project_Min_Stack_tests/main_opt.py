import datetime

clock_string = f"[{datetime.datetime.now()}]"


class MinStack:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.stack_list = []  # Stack to store all values
        self.min_stack = []  # Stack to store the minimum values
        self.head = 0

    def push(self, val: int) -> None:
        """
        Push element val onto stack.
        Not use numpy.min(self.min_stack = []) because this is O(N)
        """
        self.stack_list.append(val)
        # upgrade the minimum to be compliance with O(1) and not O(N)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)
        self.head += 1

    def pop(self) -> None:
        """
        Removes the element on the top of the stack.
        """
        try:
            if self.head > 0:
                if self.stack_list[-1] == self.min_stack[-1]:
                    self.min_stack.pop()
                self.stack_list.pop()
                self.head -= 1
            else:
                raise ValueError(f"{clock_string} Error during pop: The stack is empty.")
        except Exception as e:
            print(e)

    def top(self) -> int:
        """
        Get the top element.
        """
        if self.head == 0:
            raise ValueError(f"{clock_string} Error during top: The stack is empty.")
        return self.stack_list[self.head-1]

    def getMin(self) -> int:
        """
        Retrieve the minimum element in the stack.
        Time complexity: O(1)
        """
        if not self.min_stack:
            raise ValueError(f"{clock_string} Error during getMin: The stack is empty.")
        return self.min_stack[-1]

    @staticmethod
    def display_obj(obj_attr_dict: dict):
        """
        Display object attributes.
        """
        for key, val in obj_attr_dict.items():
            print(f"{key} : {val}")


if __name__ == '__main__':
    obj = MinStack()
    MinStack.display_obj(obj_attr_dict=obj.__dict__)

    obj.push(3)
    print(f"Top: {obj.top()}")  # Output: 3
    obj.push(-2)
    obj.push(4)
    obj.push(45)
    print(f"Minimum: {obj.getMin()}")  # Output: -2

    obj.pop()  # Removes 45
    print(f"Top after pop: {obj.top()}")  # Output: 4
    print(f"Minimum after pop: {obj.getMin()}")  # Output: -2
