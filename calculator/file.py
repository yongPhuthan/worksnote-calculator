from django import forms
from django.forms import widgets
from django.forms.fields import FileField

class File(forms.Form):
    file = forms.FileField(required=True, label="อัพโหลดไฟล์")