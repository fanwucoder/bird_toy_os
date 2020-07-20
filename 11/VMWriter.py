class VMWriter(object):
    def __init__(self, output):
        pass

    def write_push(self, segment, index):
        pass

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
        pass

    def write_return(self):
        pass

    def close(self):
        pass
