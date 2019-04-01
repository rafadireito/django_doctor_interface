from django import forms


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
            if field_name != 'photo':
                field.widget.attrs['placeholder'] = field.help_text
                field.widget.attrs['class'] = 'form-control'

    name = forms.CharField(label="Name", help_text="Insert doctor name")
    contact = forms.IntegerField(label="Contact", help_text="Insert doctor contact")
    email = forms.EmailField(label="Email", help_text="Insert doctor email")
    photo = forms.ImageField(label="Photo")
