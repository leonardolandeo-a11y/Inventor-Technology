from django import forms  
from django.contrib.auth.forms import UserCreationForm
from .models import Ticket,Report,CustomUser

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required= True)
    ROL_CHOICES = (("worker", "Worker"),("boss","Boss"))
    
    rol = forms.ChoiceField(choices=ROL_CHOICES,label="Rol del usuario")
    
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email", "password1","password2"]
    
    def save(self ,commit = True):
        user = super().save(commit=False)
        rol = self.cleaned_data["rol"]
        if rol == "worker":
            user.is_worker = True
        if rol == "boss":
            user.is_boss = True
        if commit == True:
            user.save()
        return user

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["worker","title","description","due_date"]
        widgets = {"due_date": forms.DateTimeInput(attrs={"type":"datetime-local"},format="%Y-%m-%dT%H:%M")}
    
class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ["description","evidence"]