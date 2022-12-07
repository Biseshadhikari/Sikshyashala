from dataclasses import fields
from django import forms 
from django.forms import ModelForm
from .models import Course, lessons
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField


class CourseForm(ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))   

    class Meta:

        model = Course
        exclude = ['slug','author']
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),'body':forms.Textarea(attrs={'class':'form-control'}),}
class LessonForm(ModelForm):
    class Meta:

        model = lessons
        fields = '__all__'
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),'body':forms.Textarea(attrs={'class':'form-control'}),}
class signupForm(UserCreationForm):
    password1 = forms.CharField(label = 'Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label = 'Confirm Password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model  = User
        fields = ['username','first_name','last_name','email']
        labels = {'first_name':'First Name','last_name':'Last Name','email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),'first_name':forms.TextInput(attrs={'class':'form-control'}),
        'last_name':forms.TextInput(attrs={'class':'form-control'}),'email':forms.TextInput(attrs={'class':'form-control'})}
        
class signinForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))
    password = forms.CharField(label= 'Password',strip  =False,widget=forms.PasswordInput(attrs = {'class':'form-control','autocomplete':'current-password'}))