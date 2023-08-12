from django import forms
from django.forms import SelectDateWidget, TextInput, RadioSelect, EmailField

from .models import User

class UserForm(forms.ModelForm):
    # conf_password = forms.CharField(max_length="100",widget={'type':'password'})
    CHOICES = [('male','male'),('female','female'),('others','others')]
    gender=forms.CharField(label='Gender', widget=forms.RadioSelect(choices=CHOICES), initial="male")
 
    class Meta:
        model = User
        fields = ['email','full_name','gender','date_of_birth','password']
        
        widgets = {
            

		'full_name':TextInput(attrs={
			'class': 'form-control',
			'placeholder':'enter name',
            
			}),
        'gender':RadioSelect(attrs={
            'class' : 'form-control form-check-input',
			'selected':'male'
			}),
        
        'date_of_birth':TextInput(attrs={
            'type':'date'
			}),
        'password':TextInput(attrs={
            'type':'password'
			}),
        }