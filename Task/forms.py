# forms.py faylini shunday ko'rinishga keltiring:
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # 'status' maydonini ham qo'shdik
        fields = ['title', 'description', 'priority', 'deadline']
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control shadow-sm', 'placeholder': 'Vazifa nomi...'}),
            'description': forms.Textarea(attrs={'class': 'form-control shadow-sm', 'placeholder': 'Batafsil tavsif...', 'rows': 4}),
            'priority': forms.Select(attrs={'class': 'form-select shadow-sm'}),
            'deadline': forms.DateTimeInput(attrs={'class': 'form-control shadow-sm', 'type': 'datetime-local'}),
            'status': forms.Select(attrs={'class': 'form-select shadow-sm'}), # Status uchun select input
        }