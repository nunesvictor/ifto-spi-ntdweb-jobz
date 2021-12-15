from core.models import Vaga
from django import forms


class VagaModelForm(forms.ModelForm):
    class Meta:
        model = Vaga
        exclude = ('candidatos',)
