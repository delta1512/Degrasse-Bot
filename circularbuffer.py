class CB:
    buff = []
    def __init__(self, string):
        self.buff = [i for i in string]
    def circulate(self):
        self.buff.append(self.buff.pop(0))
    def getString(self):
        return ''.join(self.buff)