from django import forms
    
class MeetForm(forms.Form):
    code = forms.CharField(label = 'Code', min_length=6, widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[A-Za-z0-9]+', 'title':'Enter AlphaNumerical Characters Only '}))

class FileForm(forms.Form):
    file = forms.FileField(label = 'File Name')    