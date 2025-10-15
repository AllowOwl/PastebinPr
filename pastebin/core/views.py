from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    return HttpResponse("Home page")

def paste_list(request):
    return HttpResponse("List of pastebins")

def paste_detail(request, paste_id):
    return HttpResponse(f"Details of paste - {paste_id}")