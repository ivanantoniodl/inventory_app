from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse 
from django.contrib.auth.decorators import login_required   
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class VentaView(TemplateView):
    template_name = 'ventas.html'

@login_required
def bienvenida(request):
    if request.method == 'GET':
        return HttpResponse("Bienvenido a la página principal")
    elif request.method == 'PUT':
        return HttpResponse("Bienvenido a la página principal - POST")
    else:
        return HttpResponse("Método no permitido", status=405)


def contacto(request,correo):
    return HttpResponse("Se  enviará un correo a la dirección: "+correo)  

def about(request):
    return render(request, 'home.html')