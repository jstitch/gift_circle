from django.urls import path

from . import views

app_name = 'circulo'
urlpatterns = [
    # ex: /
    path('', views.index, name='index'),
    # ex: /5
    path('<int:circulo_id>', views.circulo, name='circulo'),
    # ex: /persona/4
    path('persona/<int:persona_id>', views.persona, name='persona'),
    # ex: /deseo/3
    path('deseo/<int:deseo_id>', views.deseo, name='deseo'),
]
