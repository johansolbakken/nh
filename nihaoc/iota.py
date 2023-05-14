class Iota:
    def __init__(self):
        self._iota = 0

    def __call__(self):
        iota = self._iota
        self._iota += 1
        return iota
