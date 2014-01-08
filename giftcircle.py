class GiftCircle(object):

    def __init__(self, fname):
        data = []
        with open(fname,"r") as f:
            for s in f.readlines():
                data.append(s.strip("\n"))
        self.data = data

    def __str__(self):
        return "\n".join(self.data)+"\n"
    
    def parse_data(self):
        self.parsed = []
        for elem in self.data:
            d = elem.split(",")
            participante = {'name'    : d[0]}
            participante['contact'] = d[1]
            self.parsed.append(participante)

        return self.parsed
