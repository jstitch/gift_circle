from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Circulo, Persona, Deseo

def index(request):
    latest_circulo_list = Circulo.objects.order_by('-nombre')[:5]
    context = {
        'latest_circulo_list': latest_circulo_list,
    }
    return render(request, 'circulo/index.html', context)

def circulo(request, circulo_id):
    un_circulo = get_object_or_404(Circulo, pk=circulo_id)
    return render(request, 'circulo/circulo.html', {'circulo': un_circulo})

def persona(request, persona_id):
    una_persona = get_object_or_404(Persona, pk=persona_id)
    return render(request, 'circulo/persona.html', {'persona': una_persona})

def deseo(request, deseo_id):
    un_deseo = get_object_or_404(Deseo, pk=deseo_id)
    return render(request, 'circulo/deseo.html', {'deseo': un_deseo})
