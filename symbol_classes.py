class base_symbol:
    """Base class for symbols in math expression"""
    id = None
    value = 0

    def nud(self):
        raise SyntaxError("Syntax Error {}".format(self))

    def led(self):
        raise SyntaxError("Syntax Error {}".format(self))

    def __repr__(self):
        if self.id == "func" or self.id == "lit":
            return "(%s %s)" % (self.id, self.value)
        out = [self.id]
        out = map(str, filter(None, out))
        return "(" + " ".join(out) + ")"