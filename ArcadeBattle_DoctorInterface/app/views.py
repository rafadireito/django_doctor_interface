from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return redirect("/general_statistics")

def all_patients(request):
    return  render(request, "all_patients.html", {})

def all_admins(request):
    return  render(request, "all_admins.html", {})

def all_doctors(request):
    return  render(request, "all_doctors.html", {})

def patient_statistics(request):
    return render(request, "patient_statistics.html", {"nif" : request.GET['nif']})

def admin_statistics(request):
    return render(request, "admin_statistics.html", {"nif" : request.GET['nif']})

def doctor_statistics(request):
    return render(request, "doctor_statistics.html", {"nif" : request.GET['nif']})

def general_statistics(request):
    return render(request, "general_statistics.html", {})

def games(request):
    return render(request, "games.html", {})

def add_patient(request):
    return render(request, "add_patient.html", {})

def add_admin(request):
    return render(request, "add_admin.html", {})

def add_doctor(request):
    return render(request, "add_doctor.html", {})