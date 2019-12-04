# coding: utf-8

import random, datetime
try:
    from . import send_ticket as st
except ImportError:
    import send_ticket as st

def load_data(fname):
    data = []
    with open(fname,"r") as f:
        for l in f.readlines():
            if l.strip()[0] == "#": continue
            data.append(l.strip("\n"))
    return data

def parse_data(lista):
    data = []
    for elem in lista:
        d = elem.split(",")
        participant = {'name' : d[0]}
        participant['contact'] = []
        participant['gifts'] = []
        for e in d[1:]:
            e.strip()
            try:
                c = e[:]
                int(c.replace("-","").replace("+","").replace(" ","").replace("(","").replace(")",""))
                participant['contact'].append({'dest':e, 'type':"SMS"})
            except ValueError:
                if '@' in e:
                    participant['contact'].append({'dest':e, 'type':"Email"})
                else:
                    participant['gifts'].extend(e.split(";"))
        data.append(participant)
    return data

def shuffle_data(data, validate=False):

    def validate_data(data):
        for elem in data[0]['contact']:
            if elem['dest'] in [ dest['dest'] for dest in data[-1]['contact'] ]:
#                print("Failed validation!")
                return False
        for elem,antelem in zip(data[1:],data[:-1]):
            for cont in elem['contact']:
                if cont['dest'] in [ dest['dest'] for dest in antelem['contact'] ]:
#                    print("Failed validation!")
                    return False
        # TODO: do not allow inner loops
        return True

    random.shuffle(data)

    while not validate_data(data):
        if validate: return False
        random.shuffle(data)

    return data

def enviar(data):
    for n,e in enumerate(data):
        desde = e
        try:
            to = data[n + 1]
        except IndexError as ierr:
            to = data[0]
        print(n,desde['name'],to['name'])
        for destiny in desde['contact']:
            try:
                senderclass = getattr(st,destiny['type'])
            except AttributeError as aerr:
                raise Exception("Sending type not recognized: %s (%s) for %s" % (destiny['type'],destiny['dest'],desde['name']))
            regalos = "\n-".join(to['gifts'])
            if len(to['gifts']) > 1:
                regalos = regalos[0:regalos.rfind("\n")] + "\no\n" + regalos[regalos.rfind("\n")+1:]
            mensaje = "Hola %s!\nPara el intercambio te toco %s, que le gustaría recibir uno de lo siguiente:\n\n-%s.\n\nObsequios con un rango de $200 a $300\n\nfecha: Martes 24/Dic/2013" % (desde['name'],to['name'],regalos)
            sender = senderclass("","",destiny['dest'],desde['name'],mensaje)
            sender.send()

if __name__=="__main__":
    import argparse, sys, pprint

    parser = argparse.ArgumentParser(description="")
    parser.add_argument("filename", help="")
    parser.add_argument("--results", help="", action="store_true")

    args = parser.parse_args()

    if args.filename:
        if not args.results:
            d = shuffle_data(parse_data(load_data(args.filename)))
            pprint.pprint(d)
            f = open("result_%s" % datetime.datetime.now().isoformat(), "wt")
            f.write(str(d))
            f.close()
        else:
            f = open(args.filename, "r")
            cont = f.read()
            f.close()
            import ast
            d = ast.literal_eval(cont)
            pprint.pprint(d)

        cont = False
        enviar(d)

    sys.exit(0)
