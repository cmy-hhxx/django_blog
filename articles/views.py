from django.shortcuts import render
from django.http import HttpResponse

def articles_list(request):
    return HttpResponse("hello there")

