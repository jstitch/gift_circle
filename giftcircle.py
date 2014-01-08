class GiftCircle(object):

    def __init__(self, fname):
        data = ""
        with open(fname,"r") as f:
            data = f.read()
        self.data = data

    def __str__(self):
        return self.data
