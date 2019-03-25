from django.shortcuts import render

# Create your views here.

def index(request):
    return  render(request, "basic_layout.html", {})

def all_patients(request):
    return  render(request, "all_patients.html", {})
