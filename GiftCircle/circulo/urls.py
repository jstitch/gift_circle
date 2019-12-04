from django.urls import path

from . import views

app_name = 'circulo'
urlpatterns = [
    # ex: /
    path('', views.IndexView.as_view(), name='index'),
    # ex: /5
    path('<int:pk>', views.CirculoView.as_view(), name='circulo'),
    # ex: /persona/4
    path('persona/<int:pk>', views.PersonaView.as_view(), name='persona'),
    # ex: /deseo/3
    path('deseo/<int:pk>', views.DeseoView.as_view(), name='deseo'),

    path('<int:circulo_id>/enviar_circulo', views.enviar_circulo, name='enviar_circulo'),

    path('nuevo_circulo', views.nuevo_circulo, name='nuevo_circulo'),
    path('<int:circulo_id>/nueva_persona', views.nueva_persona, name='nueva_persona'),

    path('<int:circulo_id>/eliminar_circulo', views.eliminar_circulo, name='eliminar_circulo'),
]
