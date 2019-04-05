from django.contrib import admin

# Register your models here.
from app.models import Person, Gesture, Game, Patient, GamePlayed

admin.site.register(Person)
admin.site.register(Patient)
admin.site.register(Game)
admin.site.register(Gesture)
admin.site.register(GamePlayed)
