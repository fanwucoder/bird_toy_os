class VMWriter(object):
    def __init__(self, output):
        self._out_buf = open(output, "w+")

    def write_push(self, segment, index):
        self._out_buf.write("push %s %s" % (segment, index))

    def write_pop(self, segment, index):
        pass

    def write_arithmetic(self, command):
        pass

    def write_label(self, label):
        pass

    def write_goto(self, label):
        pass

    def write_if(self, label):
        pass

    def write_call(self, name, n_args):
        pass

    def write_function(self, name, n_args):
        self._out_buf.write("function %s %s" % (name, n_args))

    def write_return(self):
        pass

    def close(self):
        self._out_buf.close()
