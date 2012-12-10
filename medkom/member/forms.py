from django import forms
from member.models import Usia, StatusSosial

class AgeForm(forms.ModelForm):
    error_css_class = 'alert alert-error'
    
    class Meta:
        model = Usia
        
class StatusSosialForm(forms.ModelForm):
    error_css_class = 'alert alert-error'
    
    class Meta:
        model = StatusSosial

class SearchForm(forms.Form):
    q = forms.CharField(required=False)