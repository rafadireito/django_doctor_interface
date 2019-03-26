from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return redirect("/statistics")

def all_patients(request):
    return  render(request, "all_patients.html", {})

def statistics(request):
    return render(request, "statistics.html", {})