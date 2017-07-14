__all__=["cal1"]

_g=None

class _Calculate(object):
    def __init__(self):
        with open('text.txt') as f:
            lines = f.readlines()
        self.lines = lines
        print('Read all information.')

    def call(self):
        print('In in _calculate.call!')
        return self.lines

if _g is None:
    _g = _Calculate()

def cal1():
    return _g.call()
