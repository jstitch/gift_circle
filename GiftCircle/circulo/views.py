from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib import messages

from .models import Circulo, Persona, Deseo


class IndexView(generic.ListView):
    template_name = 'circulo/index.html'
    context_object_name = 'latest_circulo_list'

    def get_queryset(self):
        """Return the last five circulos."""
        return Circulo.objects.order_by('-nombre')[:5]


class CirculoView(generic.DetailView):
    model = Circulo
    template_name = 'circulo/circulo.html'


class PersonaView(generic.DetailView):
    model = Persona
    template_name = 'circulo/persona.html'


class DeseoView(generic.DetailView):
    model = Deseo
    template_name = 'circulo/deseo.html'


def enviar_circulo(request, circulo_id):
    un_circulo = get_object_or_404(Circulo, pk=circulo_id)
    if not un_circulo.shuffeled:
        if len(un_circulo.persona_set.all()) < 3:
            messages.add_message(request, messages.INFO, 'Debe haber por lo menos tres personas para que el juego valga la pena.')
        else:
            lista = []
            for persona in un_circulo.persona_set.all():
                elem = "{},".format(persona.nombre.replace(","," "))
                for deseo in persona.deseo_set.all():
                    elem += "{};".format(deseo.deseo)
                elem.strip(";")
                if persona.telefono:
                    elem += ",{}".format(persona.telefono)
                elif persona.email:
                    elem += ",{}".format(persona.email)
                lista.append(elem)

            if lista:
                from gift_circle import gift_circle as gf
                gf.enviar(gf.shuffle_data(gf.parse_data(lista)))

                un_circulo.shuffeled = True
                un_circulo.save()

    return HttpResponseRedirect(reverse('circulo:circulo', args=(circulo_id,)))


def nuevo_circulo(request):
    circulo = Circulo(nombre=request.POST['nombre'])
    circulo.save()
    return HttpResponseRedirect(reverse('circulo:index'))


def nueva_persona(request, circulo_id):
    circulo = get_object_or_404(Circulo, pk=circulo_id)

    if not request.POST['telefono'] and not request.POST['email']:
        messages.add_message(request, messages.INFO, 'Debe especificar al menos un medio de contacto.')
    else:
        nombre = Persona(nombre=request.POST['nombre'], telefono=request.POST['telefono'], email=request.POST['email'])
        nombre.circulo = circulo
        nombre.save()

    return HttpResponseRedirect(reverse('circulo:circulo', args=(circulo.id,)))


def eliminar_circulo(request, circulo_id):
    circulo = get_object_or_404(Circulo, pk=circulo_id)

    circulo.delete()
    return HttpResponseRedirect(reverse('circulo:index'))
