from django import forms
from .models import UserFiles


# class UploadFileForm(forms.Form):
#     file_name = forms.CharField(max_length=50)
#     file = forms.FileField(label="Select a file")


class FileForm(forms.ModelForm):
    class Meta:
        model = UserFiles
        fields = ('file',)