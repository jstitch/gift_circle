from django.urls import path

from . import views

app_name = 'circulo'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),

    path('<int:pk>', views.CirculoView.as_view(), name='circulo'),
    path('persona/<int:pk>', views.PersonaView.as_view(), name='persona'),
    path('deseo/<int:pk>', views.DeseoView.as_view(), name='deseo'),

    path('<int:circulo_id>/enviar_circulo', views.enviar_circulo, name='enviar_circulo'),

    path('nuevo_circulo', views.nuevo_circulo, name='nuevo_circulo'),
    path('<int:circulo_id>/nueva_persona', views.nueva_persona, name='nueva_persona'),
    path('<int:persona_id>/nuevo_deseo', views.nuevo_deseo, name='nuevo_deseo'),

    path('<int:circulo_id>/eliminar_circulo', views.eliminar_circulo, name='eliminar_circulo'),
    path('<int:persona_id>/eliminar_persona', views.eliminar_persona, name='eliminar_persona'),
    path('<int:deseo_id>/eliminar_deseo', views.eliminar_deseo, name='eliminar_deseo'),
]
