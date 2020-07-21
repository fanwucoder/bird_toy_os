class VMWriter(object):
    def __init__(self, output):
        self._out_buf = open(output, "w+")

    def write_push(self, segment, index):
        self._out_buf.write("push %s %s\n" % (segment, index))

    def write_pop(self, segment, index):
        pass

    def write_arithmetic(self, command):
        # 不包括算数术取反
        if command == "+":
            command = "add"
        elif command == "-":
            command = "sub"
        elif command == "*":
            self.write_call("Math.multiply", 2)
            return
        elif command == "/":
            self.write_call("Math.divide", 2)
            return
        self._out_buf.write("%s \n" % command)

    def write_label(self, label):
        pass

    def write_goto(self, label):
        pass

    def write_if(self, label):
        pass

    def write_call(self, name, n_args):
        self._out_buf.write("call %s %s \n" % (name, n_args))

    def write_function(self, name, n_args):
        self._out_buf.write("function %s %s\n" % (name, n_args))

    def write_return(self):
        self._out_buf.write("return \n")

    def close(self):
        self._out_buf.close()
