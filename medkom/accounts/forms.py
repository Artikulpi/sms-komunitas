from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class NewUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, label="Nama Depan")
    last_name = forms.CharField(max_length=30, required=False, label="Nama Belakang")
    email = forms.EmailField(required=False, label="Alamat E-Mail")
    is_superuser = forms.BooleanField(required=False, label="Admin?")
    is_staff = forms.BooleanField(required=False, label="Staff?")
    
    error_css_class = "alert alert-error"
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.is_superuser = self.cleaned_data["is_superuser"]
        user.is_staff = self.cleaned_data["is_staff"]
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save()
            
        return user

class EditUserForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=False, label="Nama Depan")
    last_name = forms.CharField(max_length=30, required=False, label="Nama Belakang")
    email = forms.EmailField(required=False, label="Alamat E-Mail")
    is_superuser = forms.BooleanField(required=False, label="Admin?")
    is_staff = forms.BooleanField(required=False, label="Staff?")
    
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(EditUserForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.populate()
    
    def save(self, commit=True):
        self.instance.first_name = self.cleaned_data["first_name"]
        self.instance.last_name = self.cleaned_data["last_name"]
        self.instance.email = self.cleaned_data["email"]
        self.instance.is_super_user = self.cleaned_data["is_superuser"]
        self.instance.is_staff = self.cleaned_data["is_staff"]
        
        if commit:
            self.instance.save()
            
        return self.instance
    
    def populate(self):
        self.fields['first_name'].initial = self.instance.first_name
        self.fields['last_name'].initial = self.instance.last_name
        self.fields['email'].initial = self.instance.email
        self.fields['is_superuser'].initial = self.instance.is_superuser
        self.fields['is_staff'].initial = self.instance.is_staff
        
