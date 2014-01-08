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
        self.parsed = [{'name'    : "Javier Novoa Cataño",
                        'contact' : "jstitch@gmail.com"},
                       {'name'    : "Javier Naranjamecanica",
                        'contact' : "naranjamecanica00@hotmail.com"},
                      ]

        return self.parsed
