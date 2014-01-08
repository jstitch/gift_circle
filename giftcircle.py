class GiftCircle(object):

    def __init__(self, fname):
        data = []
        with open(fname,"r") as f:
            for s in f.readlines():
                data.append(s.strip("\n"))
        self.data = data

    def __str__(self):
        return self.data
