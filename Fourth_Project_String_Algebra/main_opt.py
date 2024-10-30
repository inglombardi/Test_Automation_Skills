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
        # ===  Digit detection  ===
        for wk in possile_words:
            # Startswith is an optimization of the code
            if sample_str.startswith(wk, k):
                digit_buffer.append(str_int_lookup_table[wk]) # match + push
                k += len(wk) # upgrade the index (offset)
                matching = True # bool
                break # threshold optimization
        # === Operand detection ===
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
                if not matching:
                    raise ValueError(f"Unrecognized token {op} in input string {sample_str}")
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
    Convert an integer to its written-out string form, handling both positive and negative numbers.
    Example: -1 -> 'minusone'
    """
    exp = ''
    if int_v < 0:
        exp += 'minus'
        int_v = abs(int_v)

    # like unpacking: d_k is the k_th digit
    int_list = [int(d_k) for d_k in str(int_v)]
    possile_digits = list(int_str_lookup_table.keys())
    for d_k in int_list:
        if d_k in possile_digits:
            exp += int_str_lookup_table[d_k]
    return exp


if __name__ == '__main__':
    frame_sample_str = [
        'oneplusoneplusone',
    ]
    expected_res = ['three']

    c = calculator.Calculator()
    print("\n\n=============== ")
    for i, el in enumerate(frame_sample_str):
        template = eval_str(sample_str=el)

        result = template[0]
        for j in range(1, len(template), 2): # Removing operands
            # digits ==> even
            # operands ==> odd
            function_pointer = getattr(strategy, template[j])
            result = function_pointer(result, template[j + 1])

        str_res = eval_integer(int_v=result)
        pass_or_fail = str_res == expected_res[i]
        print(f"TEST num.{i + 1}: {el} ==>  {result} ==>  {str_res} ==> PASS: {pass_or_fail}")