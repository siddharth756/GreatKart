from django import forms
from .models import Account, UserProfile

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class' : 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password',
        'class' : 'form-control'
    }))
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number','password']
        # widgets = {
        #     'first_name': forms.TextInput(attrs={
        #         'class': 'form-control'
        #     })
        # }
    
    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Firstname'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Lastname'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        for fields in self.fields:
            self.fields[fields].widget.attrs['class'] = 'form-control'
            
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password must be match with confirm password."
            )   


class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number']

    def __init__(self, *args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs) 
        for fields in self.fields:
            self.fields[fields].widget.attrs['class'] = 'form-control'  

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages = {'Invalid': ('Image files only.')}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ['address_line_1','address_line_2','city','state','country','profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm,self).__init__(*args, **kwargs) 
        for fields in self.fields:
            self.fields[fields].widget.attrs['class'] = 'form-control'  