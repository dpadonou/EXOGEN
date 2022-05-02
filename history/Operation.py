class Operation(object):
    def __init__(self, op_type, trans_number, var=None):
        self.op_type = op_type
        self.trans_number = trans_number
        self.var = var

    def show(self):
        name = self.op_type + str(self.trans_number) + "(" + str(
            self.var) + ")" if self.op_type != 'c' else self.op_type + str(self.trans_number)
        return name
