from typing import Any, Dict, Tuple

from core.models import Candidato, Contato, Endereco
from django import forms
from django.contrib.auth.models import User


class CandidatoModelForm(forms.ModelForm):
    class Meta:
        model = Candidato
        exclude = ('user', 'experiencias', 'endereco', 'contato',)
        widgets = {
            'data_expedicao': forms.TextInput(attrs={'type': 'date'})
        }

    def __init__(self, *args: Tuple, **kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        user_fields = forms.fields_for_model(
            User, fields=('first_name', 'last_name', 'username',))
        self.fields.update(user_fields)

        endereco_fields = forms.fields_for_model(
            Endereco, exclude=('candidato', 'empresa',))
        self.fields.update(endereco_fields)

        contato_fields = forms.fields_for_model(
            Contato, exclude=('candidato', 'empresa',))
        self.fields.update(contato_fields)

        self.order_fields(('first_name', 'last_name', 'username'))

        if self.instance.pk:
            self.fields['username'].widget.attrs.update({'readonly': 'readonly'})
