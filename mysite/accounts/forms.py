from django import forms

class SignupForm(forms.Form):
    firstname = forms.CharField(label = 'First name')
    surname = forms.CharField(label = 'Surname')
    email = forms.EmailField(label='Email address')
    password = forms.CharField(label = 'Password', min_length=8)
    repassword = forms.CharField(label = 'Retype Password', min_length=8)
    
    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        password = cleaned_data.get("password")
        repassword = cleaned_data.get("repassword")
    
        if password != repassword:
            self.add_error('repassword', "Password does not match")
    
        
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(label = 'Password', min_length=8)