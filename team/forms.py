from django import forms
from .models import Teams, TeamsLeaders

class CreateTeamForm(forms.ModelForm):
    name=forms.CharField(label="Название" ,max_length=100)
    description=forms.CharField(label="Описание")
    link=forms.CharField(label="Ссылка", max_length=2048)
    url=forms.CharField(label="Ссылка-приглашение", max_length=2048, required=False, widget = forms.HiddenInput())
    class Meta:
        model=Teams
        fields=('name','description','link','url')
        

class AdminPanel(forms.BaseModelForm):
    name=forms.CharField(label="Название" ,max_length=100)
    description=forms.CharField(label="Описание")
    link=forms.CharField(label="Ссылка", max_length=2048)
    url=forms.CharField(label="Ссылка-приглашение", max_length=2048)
    score=forms.IntegerField(label="Счет")
    class Meta:
        model=Teams
        fields=('name','description','link','url','score')


