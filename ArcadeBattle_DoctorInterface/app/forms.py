from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class AddPatient(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'photo':
                field.widget.attrs['placeholder'] = field.help_text
                field.widget.attrs['class'] = 'form-control'

    name = forms.CharField(label="Name", help_text="Insert patient name")
    contact = forms.IntegerField(label="Contact", help_text="Insert patient contact")
    email = forms.EmailField(label="Email", help_text="Insert patient email")
    photo = forms.ImageField(label="Photo")

class AddAdmin(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'photo':
                field.widget.attrs['placeholder'] = field.help_text
                field.widget.attrs['class'] = 'form-control'

    name = forms.CharField(label="Name", help_text="Insert admin name")
    contact = forms.IntegerField(label="Contact", help_text="Insert admin contact")
    email = forms.EmailField(label="Email", help_text="Insert admin email")
    photo = forms.ImageField(label="Photo")


class AddDoctor(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'photo' and field_name != 'birth_date':
                field.widget.attrs['placeholder'] = field.help_text
                field.widget.attrs['class'] = 'form-control'

    first_name = forms.CharField(label="First Name", help_text="Insert doctors first name")
    last_name = forms.CharField(label="Last Name", help_text="Insert doctors last name")
    nif = forms.IntegerField(label="NIF", help_text="Insert doctor NIF")
    birth_date = forms.DateField(label="Birth Date", help_text="Insert doctor birth date",
                                 widget=forms.SelectDateWidget(years=range(1900, 2019)))
    contact = forms.IntegerField(label="Contact", help_text="Insert doctors contact")
    email = forms.EmailField(label="Email", help_text="Insert doctors email")
    photo = forms.ImageField(label="Photo", required=False)


class AddGesture(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'image':
                field.widget.attrs['placeholder'] = field.help_text
                field.widget.attrs['class'] = 'form-control'
            if field_name == 'birth_date':
                field.widget.attrs['class'] = 'col-md-3 col-sm-4'

    name = forms.CharField(label="Name", help_text="Insert the gesture name")
    default_difficulty = forms.IntegerField(label="Default difficulty", widget=forms.NumberInput(attrs={'type':'range', 'step': '1', 'value':'50', 'min': '1', 'max': '100'}), help_text="Insert the default difficulty")
    repetitions = forms.IntegerField(label="Number of repetitions", min_value=1,  help_text="Insert the number of repetitions")
    decision_tree = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'id':'jsonInputText', 'style':'display:none'}))
    gesture_image = forms.CharField(widget=forms.TextInput(attrs={'type':'text', 'id':'imageInputText', 'style':'display:none'}))


class UpdateProfile(forms.Form):
    def __init__(self, user , *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        if user != None:
            for field_name, field in self.fields.items():
                field.widget.attrs['placeholder'] = field.help_text
                field.widget.attrs['class'] = 'form-control'
                #Complete form auto
                if field_name == 'first_name':
                    field.initial = user.first_name

                if field_name == 'last_name':
                    field.initial = user.last_name

                if field_name == 'email':
                    field.initial = user.username


                if field_name == 'nif':
                    field.initial = user.person.nif

                if field_name == 'contact':
                    field.initial = user.person.contact

                if field_name == 'birth_date':
                    field.widget.attrs['class'] = 'col-md-3 col-sm-3'
                    field.initial = user.person.birth_date

                if field_name == 'photo':
                    field.widget.attrs['class'] = 'col-md-3 col-sm-3'
                    field.initial = "data:image/png;base64," + user.person.photo_b64


    first_name = forms.CharField(label="First Name", help_text="Insert doctors first name")
    last_name = forms.CharField(label="Last Name", help_text="Insert doctors last name")
    nif = forms.IntegerField(label="NIF", help_text="Insert doctor NIF")
    birth_date = forms.DateField(label="Birth Date", help_text="Insert doctor birth date",
                                 widget=forms.SelectDateWidget(years=range(1900, 2019)))
    contact = forms.IntegerField(label="Contact", help_text="Insert doctors contact")
    email = forms.EmailField(label="Email", help_text="Insert doctors email")
    photo = forms.FileField(label="Photo", required=False, widget=forms.FileInput(attrs={'onchange' : 'readFile(this)'}))