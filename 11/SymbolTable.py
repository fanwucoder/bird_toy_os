class SymbolTable(object):
    def __init__(self):

        self._s_dict = dict()
        self._s_dict_idx = dict()
        self._s_idx = 0

        self._f_dict = dict()
        self._f_dict_idx = dict()
        self._f_idx = 0

        self._v_dict = dict()
        self._v_dict_idx = dict()
        self._v_idx = 0

        self._a_dict = dict()
        self._a_dict_idx = dict()
        self._a_idx = 0

    def __str__(self):
        ret = []
        self.format_tb(ret, self._s_dict, self._s_dict_idx)
        self.format_tb(ret, self._f_dict, self._f_dict_idx)
        self.format_tb(ret, self._v_dict, self._v_dict_idx)
        self.format_tb(ret, self._a_dict, self._a_dict_idx)
        return "\n".join(ret) + "\n"

    def format_tb(self, ret, dict1, dict2):
        for k, v in dict1.items():
            ret.append("%s %s %s %s" % (k, v[1], v[0], dict2[k]))

    def start_subroutine(self):

        self._v_dict = dict()
        self._v_dict_idx = dict()
        self._v_idx = 0

        self._a_dict = dict()
        self._a_dict_idx = dict()
        self._a_idx = 0

    def define(self, name, itype, kind):
        if kind == "static":
            self._s_dict[name] = (kind, itype)
            self._s_dict_idx[name] = self._s_idx
            self._s_idx += 1
        elif kind == "field":
            self._f_dict[name] = (kind, itype)
            self._f_dict_idx[name] = self._f_idx
            self._f_idx += 1
        elif kind == "var":
            self._v_dict[name] = (kind, itype)
            self._v_dict_idx[name] = self._v_idx
            self._v_idx += 1
        elif kind == "arg":
            self._a_dict[name] = (kind, itype)
            self._a_dict_idx[name] = self._a_idx
            self._a_idx += 1

    def var_count(self, kind):
        if kind == "static":
            return self._s_idx
        elif kind == "field":
            return self._f_idx
        elif kind == "var":
            return self._v_idx
        elif kind == "arg":
            return self._a_idx
        return None

    def kind_of(self, name):
        if name in self._v_dict:
            return "var"
        elif name in self._a_dict:
            return "arg"
        elif name in self._f_dict:
            return "field"
        elif name in self._s_dict:
            return "static"

    def type_of(self, name):
        kind = self.kind_of(name)
        if kind == "static":
            return self._s_dict[name][1]
        elif kind == "field":
            return self._f_dict[name][1]
        elif kind == "var":
            return self._v_dict[name][1]
        elif kind == "arg":
            return self._a_dict[name][1]

    def index_of(self, name):
        kind = self.kind_of(name)
        if kind == "static":
            return self._s_dict_idx[name]
        elif kind == "field":
            return self._f_dict_idx[name]
        elif kind == "var":
            return self._v_dict_idx[name]
        elif kind == "arg":
            return self._a_dict_idx[name]
