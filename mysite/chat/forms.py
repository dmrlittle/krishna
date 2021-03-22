from django import forms
    
class MeetForm(forms.Form):
    code = forms.CharField(label = 'Code', min_length=6, max_length=6)