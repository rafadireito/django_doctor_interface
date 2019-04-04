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

            if photo != None:
                photo_b64 = base64.b64encode(photo.file.read())
                photo_b64 = photo_b64.decode()
            else:
                photo_b64 = "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"

            # check for unique constraints

            if list(User.objects.filter(username=email)) != []:
                error_message = "There is already a user with this email! The doctor WASN'T added to database!"
                return render(request, "add_doctor.html", {'form': form, "state":"error", "state_message":error_message})

            if list(Person.objects.filter(nif=nif)) != []:
                error_message = "There is already a user with this nif! The doctor WASN'T added to database!"
                return render(request, "add_doctor.html", {'form': form, "state":"error", "state_message":error_message})


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

            state_message = "The doctor was added to database"
            return render(request, "add_doctor.html", {'form': form,  "state":"success", "state_message":state_message})
        else:
            print("Invalid form")
    else:
        form = AddDoctor()
    return render(request, "add_doctor.html", {'form': form,  "state":None})


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