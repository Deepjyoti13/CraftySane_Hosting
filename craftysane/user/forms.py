from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, EmailInput, Select, FileInput

from user.models import UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30,label= 'User Name :')
    email = forms.EmailField(max_length=200,label= 'Email :')
    first_name = forms.CharField(max_length=100, help_text='First Name', label= 'First Name :')
    last_name = forms.CharField(max_length=100, help_text='Last Name', label= 'Last Name :')

    class Meta:
        model = User
        fields = ('username', 'email','first_name','last_name', 'password1', 'password2',)
        
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs = {"class": "form-control rounded-pill", "placeholder": "Username", "aria-label": "Username", "aria-describedby": "basic-addon1" }
        self.fields["first_name"].widget.attrs = {"class": "form-control rounded-pill", "placeholder": "First Name", "aria-label": "First Name", "aria-describedby": "basic-addon1"}
        self.fields["last_name"].widget.attrs = {"class": "form-control rounded-pill", "placeholder": "Last Name", "aria-label": "Last Name", "aria-describedby": "basic-addon1"}
        self.fields["email"].widget.attrs = {"class": "form-control rounded-pill", "placeholder": "Email", "aria-label": "Email", "aria-describedby": "basic-addon1"}
        self.fields["password1"].widget.attrs = {"class": "form-control rounded-pill", "placeholder": "Enter Password", "aria-label": "Enter Password", "aria-describedby": "basic-addon1"}
        self.fields["password2"].widget.attrs = {"class": "form-control rounded-pill", "placeholder": "Confirm Password", "aria-label": "Confirm Password", "aria-describedby": "basic-addon1"}
class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ( 'username','email','first_name','last_name')
        widgets = {
            'username'  : TextInput(attrs={'class': 'input','placeholder':'username'}),
            'email'     : EmailInput(attrs={'class': 'input','placeholder':'email'}),
            'first_name': TextInput(attrs={'class': 'input','placeholder':'first_name'}),
            'last_name' : TextInput(attrs={'class': 'input','placeholder':'last_name' }),
        }


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city','country','image')
        widgets = {
            'phone'     : TextInput(attrs={'class': 'input', 'placeholder':'phone'}),
            'address'   : TextInput(attrs={'class': 'input', 'placeholder':'address'}),
            'city'      : Select(attrs={'class': 'input', 'placeholder':'city'}),
            'PINcode'   : Select(attrs={'class': 'input', 'placeholder':'PIN code'}),
            'country'   : TextInput(attrs={'class': 'input', 'placeholder':'country' }),
            'image'     : FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
        }