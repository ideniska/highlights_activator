from django import forms
from .models import UserFiles


class FileForm(forms.ModelForm):
    class Meta:
        model = UserFiles
        fields = ("file",)
