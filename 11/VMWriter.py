cur_engine = None


class VMWriter(object):
    def __init__(self, output):
        self._out_buf = open(output, "w+")

    def set_engine(self, cur):
        global cur_engine
        cur_engine = cur

    def write_push(self, segment, index):
        self._out_buf.write("push %s %s // %s\n" % (segment, index, cur_engine.line_num()))

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
        self._out_buf.write("%s //%s\n" % (c_map[command], cur_engine.line_num()))

    def write_label(self, label):
        self._out_buf.write("label %s //%s\n" % (label, cur_engine.line_num()))

    def write_goto(self, label):
        self._out_buf.write("goto %s //%s\n" % (label, cur_engine.line_num()))

    def write_if(self, label):
        self._out_buf.write("if-goto %s //%s\n" % (label, cur_engine.line_num()))

    def write_call(self, name, n_args):
        self._out_buf.write("call %s %s //%s\n" % (name, n_args, cur_engine.line_num()))

    def write_function(self, name, n_args):
        self._out_buf.write("function %s %s //%s\n" % (name, n_args, cur_engine.line_num()))

    def write_return(self):
        self._out_buf.write("return %s\n" % cur_engine.line_num())

    def close(self):
        self._out_buf.close()

    def write_comment(self, comment):
        self._out_buf.write("//%s \n" % (comment))
