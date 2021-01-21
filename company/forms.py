from django import forms
from .models import Company

class CompanyForm(forms.ModelForm):
    name=forms.CharField(max_length=250, widget=forms.TextInput(attrs={'class':'form-control mt-1', 'placeholder':'Название'}))
    description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control mt-1', 'placeholder':'Описание'}))
    class Meta:
        model=Company
        fields=('name', 'description')
