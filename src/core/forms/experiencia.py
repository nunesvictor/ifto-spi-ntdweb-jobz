from core.models import ExperienciaProfissional
from django import forms


class ExperienciaModelForm(forms.ModelForm):
    class Meta:
        model = ExperienciaProfissional
        fields = '__all__'
        widgets = {
            'data_inicio': forms.TextInput(attrs={'type': 'date'}),
            'data_conclusao': forms.TextInput(attrs={'type': 'date'}),
            'tarefas_executadas': forms.Textarea(attrs={'rows': 3})
        }
