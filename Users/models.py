from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    is_worker = models.BooleanField(default=False)
    is_boss = models.BooleanField(default=False)
    

class Ticket(models.Model):
    boss = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="tickets_created",limit_choices_to={"is_boss":True})
    worker = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="assigned_tickets",limit_choices_to={"is_worker":True})
    title = models.CharField(max_length= 200)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null= True,blank= True)
    work_completed = models.BooleanField(default= False)
    
    STATUS_CHOICES = [
        ('to_review', 'To Review'),
        ('completed', 'Completed'),
        ('in_progress', 'In Progress'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    
    def __str__(self):
        return f"{self.title} - {self.worker.username}"
    

class Report(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="reports")
    worker = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    description = models.TextField()
    evidence = models.FileField(upload_to="uploads/",blank=True,null= True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reporte de {self.worker.username} para {self.ticket.title} otorgado por {self.ticket.boss.username}"

