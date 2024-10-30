import unittest
from datetime import datetime
from main_opt import MinStack, clock_string  # Import the module containing MinStack


class TestMinStack(unittest.TestCase):


    def setUp(self):
        """
        Set up a fresh instance of MinStack for each test.
        Sample for testing just to check if the Module create the data structure
        """
        self.stack = MinStack()
        self.first_elem = 3
        self.second_elem = -2

    def test_push(self):
        """
        Test if push correctly adds elements to the stack. Consider that the Push Test depends strictly by Top
        """
        self.stack.push(self.first_elem)
        self.assertEqual(self.stack.top(), self.first_elem)  # Verify top element is correct
        self.stack.push(self.second_elem)
        self.assertEqual(self.stack.top(), self.second_elem)  # Verify the top is updated after push
        self.stack.push(self.first_elem**2)
        self.stack.push(self.second_elem**2)
        self.assertEqual(self.stack.top(), self.second_elem**2)  # Verify after multiple pushes

    def test_pop(self):
        """
        Test if pop correctly removes elements from the stack.
        """
        self.stack.push(self.first_elem)
        self.stack.push(self.second_elem)
        self.stack.pop()
        self.assertEqual(self.stack.top(), self.first_elem)  # Verify after pop

        # Test pop on empty stack, should raise ValueError
        self.stack.pop()  # stack becomes empty
        with self.assertRaises(ValueError):
            self.stack.pop()

    def test_top(self):
        """
        Test if top correctly returns the top element of the stack.
        """
        self.stack.push(self.first_elem)
        self.assertEqual(self.stack.top(), self.first_elem)
        self.stack.push(self.second_elem)
        self.assertEqual(self.stack.top(), self.second_elem)

        # Test top on an empty stack, should raise ValueError
        self.stack.pop()
        self.stack.pop()  # empty stack
        with self.assertRaises(ValueError):
            self.stack.top()

    def test_getMin(self):
        """
        Test if getMin correctly returns the minimum element in the stack.
        """
        first = self.first_elem # 3
        second = self.second_elem # -2
        third = self.first_elem**2 # 9
        fourth = self.second_elem**2 # 4
        self.stack.push(first)
        self.stack.push(second)
        self.stack.push(third)
        self.assertEqual(self.stack.getMin(), second)  # Minimum element should be -2
        self.stack.push(fourth)
        self.stack.pop()  # Removes 4
        self.assertEqual(self.stack.getMin(), second)  # Minimum remains -2

        self.stack.pop()
        self.stack.pop()
        self.stack.pop()  # Stack becomes empty

        # Test getMin on empty stack, should raise ValueError
        with self.assertRaises(ValueError): # ValueError is expected
            self.stack.getMin()

    def test_display_obj(self):
        """
        Test the static method display_obj by verifying output is correctly formatted.
        """
        # Capture the display output using a mock
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        MinStack.display_obj(obj_attr_dict=self.stack.__dict__)
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        self.assertIn('stack_list', output)
        self.assertIn('min_stack', output)
        self.assertIn('head', output)


if __name__ == '__main__':
    unittest.main()
