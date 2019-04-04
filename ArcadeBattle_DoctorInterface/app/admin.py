from django.contrib import admin

# Register your models here.
from app.models import Person, Gestures

admin.site.register(Person)
admin.site.register(Gestures)

