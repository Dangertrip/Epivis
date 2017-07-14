__all__=["cal1"]

_g=None

class _Calculate(object):
    def __init__(self):
#        with open('text.txt') as f:
#            lines = f.readlines()
        self.lines = [1,2,3,4,5,6,7,8,9]
        print('Read all information.')

    def call(self):
        print('In in _calculate.call!')
        return self.lines

if _g is None:
    _g = _Calculate()

def cal1():
    return _g.call()
