import strategy
class Calculator(object):

    def __int__(self, f_op):
        """
        :param f_op: f_op_char_extracted_from_sample_string in ['plus', 'minus', 'mul', 'div']
        :return:
        Strategy pattern:
        Logic: str_op = {'plus': '+', 'minus': '-', 'mul': '*', 'div': ':'}

        """
        self.cumulative_total = 0
        # default strategy
        self._eval_expression = strategy.f_plus # the strategy storages a pointer


    def result(self, a: int, b:int) -> int:
        self.cumulative_total += self.eval_expression(a, b)

    def get_result(self):
        return self.cumulative_total

    @property
    def eval_expression(self):
        return self._eval_expression

    @eval_expression.setter
    def eval_expression(self, f_op):
        self._eval_expression = f_op

