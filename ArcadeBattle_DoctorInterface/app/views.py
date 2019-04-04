import base64
import smtplib
import ssl

from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from app.forms import AddPatient, AddAdmin, AddDoctor, AddGesture, UpdateProfile
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
from app.models import Person, Gestures


def index(request):
    # if user is not authenticaded -> login
    if not request.user.is_authenticated:
        return redirect("login")

    return redirect("/general_statistics")


def all_patients(request):
    # if user is not a doctor or isnt authenticated-> login
    if not request.user.is_authenticated or (request.user.username != "admin" and request.user.groups.all()[0].name not in ["doctors_group"] ):
        return redirect("login")
    return render(request, "all_patients.html", {})


def all_admins(request):
    # if user is not an admin or isnt authenticated-> login
    if not request.user.is_authenticated or  request.user.username != "admin":
        return redirect("login")
    return  render(request, "all_admins.html", {})


def all_doctors(request):
    if not request.user.is_authenticated or (request.user.username != "admin" and request.user.groups.all()[0].name not in ["doctors_group"] ):
        return redirect("login")
    return  render(request, "all_doctors.html", {})

@csrf_exempt
def patient_statistics(request):
    if not request.user.is_authenticated or (request.user.username != "admin" and request.user.groups.all()[0].name not in ["doctors_group"] ):
        return redirect("login")

    if request.method == 'POST':
       form = AddGesture(request.POST, request.FILES)
       if form.is_valid():
            print(form.cleaned_data)
            g = Gestures(pacientID=1, name=form.cleaned_data["name"], image=form.cleaned_data["gesture_image"], repetitions=form.cleaned_data["repetitions"],
            default_difficulty=form.cleaned_data["default_difficulty"], decision_tree=form.cleaned_data["decision_tree"])
            g.save()
            form = AddGesture()
            return render(request, "patient_statistics.html", {"form": form, "nif": request.GET['nif']})
       else:
            print("Invalid form")
    else:
       form = AddGesture()
    return render(request, "patient_statistics.html", {"form":form, "nif" : request.GET['nif']})


def admin_statistics(request):
    if not request.user.is_authenticated or  request.user.username != "admin":
        return redirect("login")
    return render(request, "admin_statistics.html", {"nif" : request.GET['nif']})


def doctor_statistics(request):
    if not request.user.is_authenticated or (request.user.username != "admin" and request.user.groups.all()[0].name not in ["doctors_group"] ):
        return redirect("login")
    return render(request, "doctor_statistics.html", {"nif" : request.GET['nif']})

def general_statistics(request):
    # if user is not authenticaded -> login
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "general_statistics.html", {"user":request.user})


def games(request):
    # if user is not authenticaded -> login
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "games.html", {})


@csrf_exempt
def add_patient(request):
    # if user is not an admin not a doctor and isnt authenticated-> login
    if not request.user.is_authenticated or (request.user.username != "admin" and request.user.groups.all()[0].name not in ["doctors_group"] ):
        return redirect("login")

    if request.method == 'POST':
        form = AddPatient(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form = AddPatient()
            return render(request, "add_patient.html", {'form':form})
        else:
            print("Invalid form")
    else:
        form = AddPatient()
    return render(request, "add_patient.html", {'form':form})


@csrf_exempt
def add_admin(request):
    # if user is not an admin or isnt authenticated-> login
    if not request.user.is_authenticated or request.user.username != "admin":
        return redirect("login")

    if request.method == 'POST':
        form = AddAdmin(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)
            form = AddAdmin()
            return render(request, "add_admin.html", {'form': form})
        else:
            print("Invalid form")
    else:
        form = AddAdmin()
    return render(request, "add_admin.html", {'form': form})


@csrf_exempt
def add_doctor(request):
    # if user is not an admin or isnt authenticated-> login
    if not request.user.is_authenticated or request.user.username != "admin":
        return redirect("login")

    if request.method == 'POST':
        form = AddDoctor(request.POST, request.FILES)

        if form.is_valid():
            # get info form form
            form_data = form.cleaned_data
            first_name = form_data["first_name"]
            last_name = form_data["last_name"]
            contact = form_data["contact"]
            email = form_data["email"]
            photo = form_data["photo"]
            birth_date = form_data["birth_date"]
            nif = form_data["nif"]

            photo_b64 = base64.b64encode(photo.file.read())
            photo_b64 = photo_b64.decode()

            # create a user
            u = User.objects.create_user(username=email, first_name=first_name, last_name=last_name, password='pw')
            u.save()

            # link the user to a person
            p = Person.objects.create(user=u, contact=contact, nif=nif, birth_date=birth_date, photo_b64=photo_b64)
            p.save()

            # check if the group doctors exists, else create it
            # finally add doctor to group
            doctors_group = list(Group.objects.filter(name='doctors_group'))

            if len(doctors_group) == 0:
                doctors_group = Group.objects.create(name='doctors_group')
                doctors_group.save()

            doctors_group = Group.objects.get(name='doctors_group')
            doctors_group.user_set.add(u)

            form = AddDoctor()
            return render(request, "add_doctor.html", {'form': form})
        else:
            print("Invalid form")
    else:
        form = AddDoctor()
    return render(request, "add_doctor.html", {'form': form})


@csrf_exempt
def about(request):
    if not request.user.is_authenticated:
        return redirect("login")

    user = request.user

    if request.method == 'POST':
        form = UpdateProfile(None, request.POST, request.FILES)
        print(form)
        if form.is_valid():
            # get info form form
            form_data = form.cleaned_data
            first_name = form_data["first_name"]
            last_name = form_data["last_name"]
            contact = form_data["contact"]
            email = form_data["email"]
            photo = form_data["photo"]
            birth_date = form_data["birth_date"]
            nif = form_data["nif"]

            # get user and udate it
            u = User.objects.filter(username=email)
            u.update(first_name=first_name, last_name=last_name)

            # get user and udate it
            p = Person.objects.filter(user=u[0])
            p.update(user= u[0], contact=contact, nif=nif, birth_date=birth_date)

            # if there is a photo to update
            if photo != None:
                photo_b64 = base64.b64encode(photo.file.read())
                photo_b64 = photo_b64.decode()
                p = p.update(photo_b64=photo_b64)



            return redirect("/")
        else:
            print("Invalid form")
            print(messages.error(request, "Error"))
    else:
        form = UpdateProfile(user)

    return render(request, "about.html", {'form': form})



def send_email(request):
    res = send_mail("Hello", "Your password is 123", "arcade.battle@outlook.com", ["rafael.neves.direito@ua.pt"], fail_silently=False)
    return HttpResponse('%s' % res)


def login(request):
    return render(request, "login.html", {})