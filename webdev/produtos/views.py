from django.shortcuts import render
from django.http import HttpResponse

def estoque(request):
    return HttpResponse('Estoque de produtos')