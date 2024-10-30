""" [NAIVE SOLUTION: with result > 0 and only two operands ]
Have the function(sample_str): realize these requirements.
    - YOU CANNOT use the eval() builtins of Python

	-read the sample_str parameter being passed which will contain the written out version
     of an operation between two digits 0-9 and 0-9, or more, and convert the expression into an
     actual final mathematical result.
     'onezeropluseight' => 10+8 = 18 ==> Output: eight

    -Word Tokenization: Splitting a sentence into individual words
     In 'onezeroplusheight' there are 'one' + 'zero' + '+' + '8'

     -- Two conversion are needed --
     sample_str ==>  f1() ===> result in digit ===>  f2() ===> result in string

==============================
DOCUMENTATION ABOUT BUILTINS
==============================
txt = "Hello, welcome to my world."
print(txt.startswith("Hello")) # Output: True
print(txt.startswith("world")) # Output: False

first_text_compared.startswith(second_text_compared, lower_bound or start)

"""

import calculator
from data_structures import str_int_lookup_table, possible_operand, int_str_lookup_table
import strategy

def integer_concatenation(integer_buffer) -> int:
    """
    l = [1, 0]
    integer_concatenation(integer_buffer=l)
        10
    :param integer_buffer: string converted in list with single integer digits, integer_buffer[i] is a digit.
    :return: single concat integer
    """
    # l = [1, 0] in l = [10] before 'plus' or others
    return int("".join(map(str, integer_buffer)))


# =====================================
# f1(): sample_str ===> result in digit
# =====================================
def eval_str(sample_str: str) -> list:
    """
    :param sample_str: written out version of an operation between AT LEAST two digits 0-9 and 0-9
    :return: i.e. 'onezeropluseight' -> [10, 'f_plus', 8]
    """
    exp = []
    digit_buffer = []

    k = 0 # wk -> each token of sample_str
    possile_words = list(str_int_lookup_table.keys())
    while k < len(sample_str):
        matching = False
        # =========================
        # ===  Digit detection  ===
        # =========================
        for wk in possile_words:
            # Startswith is an optimization of the code
            if sample_str.startswith(wk, k):
                digit_buffer.append(str_int_lookup_table[wk]) # match + push
                k += len(wk) # upgrade the index (offset)
                matching = True # bool
                break # threshold optimization

        # =========================
        # === Operand detection ===
        # =========================
        if not matching:
            # Digit re-arrange
            exp.append(integer_concatenation(integer_buffer=digit_buffer))
            digit_buffer = [] # flush
            # Check for operators if no number matched
            for op in possible_operand:
                if sample_str.startswith(op, k):
                    exp.append(f'f_{op}') # push the calculator name strategy function pointer
                    k += len(op) # upgrade the index
                    matching = True # bool
                    break # threshold optimization


    # residual digits
    if digit_buffer:
        exp.append(integer_concatenation(integer_buffer=digit_buffer))
    else:
        raise ValueError(f'Unknown Token -> {digit_buffer}')


    return exp

# ===========================================
# f2(): result in digit ===> result in string
# ===========================================
def eval_integer(int_v: int) -> str:
    """
    :param int_v: i.e. 18
    :return: 'oneeight'
    """
    exp = ''
    # like unpacking: d_k is the k_th digit
    int_list = [int(d_k) for d_k in str(int_v)]
    possile_digits = list(int_str_lookup_table.keys())
    for d_k in int_list:
        if d_k in possile_digits:
            exp += int_str_lookup_table[d_k]
    return exp

if __name__ == '__main__':
    frame_sample_str = [
        # test 1: 10+8
        'onezeropluseight',
        # test 2: 10-8
        'onezerominuseight',
        # test 3: 10/8 : 1 expected as result
        'onezerodiveight',
        # test 4: 1+1+1
        'oneplusoneplusone',  # expected 3
    ]
    expected_res = ['oneeight', 'two', 'one', 'three']
    c = calculator.Calculator()
    print("\n\n=============== ")
    for i, el in enumerate(frame_sample_str):
        template = eval_str(sample_str=el)
        function_pointer = getattr(strategy, template[1])
        c.eval_expression = function_pointer
        int_res = c.eval_expression(template[0], template[2])
        str_res = eval_integer(int_v=int_res)
        pass_or_fail = str_res == expected_res[i]
        print(f"TEST num.{i+1}: {el} ==>  {int_res} ==>  {str_res} ==> PASS: {pass_or_fail}")

# Note that these tests don't have negative result but this could be a problem

"""
=============== 3/4 PASSED
TEST num.1: onezeropluseight ==>  18 ==>  oneeight ==> PASS: True
TEST num.2: onezerominuseight ==>  2 ==>  two ==> PASS: True
TEST num.3: onezerodiveight ==>  1 ==>  one ==> PASS: True
TEST num.4: oneplusoneplusone ==>  2 ==>  two ==> PASS: False
"""