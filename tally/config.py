class Bunch:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

mongo = Bunch(host='127.0.0.1',
              port=27017)
