class VMWriter(object):
    def __init__(self, output):
        self._out_buf = open(output, "w+")

    def write_push(self, segment, index):
        self._out_buf.write("push %s %s\n" % (segment, index))

    def write_pop(self, segment, index):
        self._out_buf.write("pop {} {}\n".format(segment, index))

    def write_arithmetic(self, command):
        # 不包括算数术取反
        c_map = {"+": "add", "-": "sub", "~": "not", "=": "eq", ">": "gt", "<": "lt", "&": "and", "|": "or",
                 "neg": "neg"}

        if command == "*":
            self.write_call("Math.multiply", 2)
            return
        elif command == "/":
            self.write_call("Math.divide", 2)
            return
        self._out_buf.write("%s \n" % c_map[command])

    def write_label(self, label):
        self._out_buf.write("label %s\n" % label)

    def write_goto(self, label):
        self._out_buf.write("goto %s\n" % label)

    def write_if(self, label):
        self._out_buf.write("if-goto %s\n" % label)

    def write_call(self, name, n_args):
        self._out_buf.write("call %s %s \n" % (name, n_args))

    def write_function(self, name, n_args):
        self._out_buf.write("function %s %s\n" % (name, n_args))

    def write_return(self):
        self._out_buf.write("return \n")

    def close(self):
        self._out_buf.close()

    def write_comment(self, comment):
        self._out_buf.write("//%s \n" % comment)
