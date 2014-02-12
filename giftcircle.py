# coding: utf-8

import random, re

import senders

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
            data = elem.split(",")
            participante = {'name' : data[0]}
            participante['contacts'] = []
            for d in data[1:]:
                participante['contacts'].append({})
                if re.search(r"^[^@]+@[^@]+\.[^@]+", d):
                    participante['contacts'][-1]['type'] = senders.Email
                else:
                    raise Exception("'GiftCircle' bad contact")
                participante['contacts'][-1]['addr'] = d
            self.parsed.append(participante)

        return self.parsed

    def shuffle_data(self):
        self.shuffled = self.parsed[:]
        random.shuffle(self.shuffled)
        return self.shuffled

    def send_circle(self, message=""):
        import smtplib
        for n,s in enumerate(self.shuffled):
            desde = s
            try:
                hacia = self.shuffled[n + 1]
            except IndexError:
                hacia = self.shuffled[0]
            for contact in desde['contacts']:
                em = contact['type']((contact['addr'],desde['name']),
                                     "GiftCircle",
                                     "Te toca darle a %s" % (hacia['name']))
                em.send()

if __name__=="__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Circulo de Regalos")
    parser.add_argument("filename", help="Nombre del archivo con datos de los participantes")

    args = parser.parse_args()

    gc = GiftCircle(args.filename)
    gc.parse_data()
    gc.shuffle_data()
    gc.send_circle()
