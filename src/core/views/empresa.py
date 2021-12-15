from typing import Any, Dict

from core.forms.empresa import EmpresaModelForm
from core.models import Contato, Empresa, Endereco
from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.forms.models import model_to_dict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


class EmpresaListView(ListView):
    model = Empresa
    template_name = 'empresa/list.html'


class EmpresaCreateView(CreateView):
    form_class = EmpresaModelForm
    template_name = 'empresa/form.html'
    success_url = reverse_lazy('core:empresa_list')

    @transaction.atomic
    def form_valid(self, form: EmpresaModelForm) -> HttpResponse:
        empresa = form.save(commit=False)

        endereco_keys = forms.fields_for_model(Endereco, exclude=())
        endereco = Endereco.objects.create(
            **{k: form.cleaned_data[k] for k in endereco_keys})

        contato_keys = forms.fields_for_model(Contato, exclude=())
        contato = Contato.objects.create(
            **{k: form.cleaned_data[k] for k in contato_keys})

        user = User.objects.create_user(form.cleaned_data['username'])

        empresa.user = user
        empresa.endereco = endereco
        empresa.contato = contato

        empresa.save()

        return HttpResponseRedirect(self.success_url)


class EmpresaUpdateView(UpdateView):
    model = Empresa
    form_class = EmpresaModelForm
    template_name = 'empresa/form.html'
    success_url = reverse_lazy('core:empresa_list')

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()

        initial.update(model_to_dict(self.get_object().user))
        initial.update(model_to_dict(self.get_object().endereco))
        initial.update(model_to_dict(self.get_object().contato))

        return initial

    @transaction.atomic
    def form_valid(self, form: EmpresaModelForm) -> HttpResponse:
        empresa = form.save()

        endereco_keys = forms.fields_for_model(Endereco, exclude=())
        Endereco.objects.filter(pk=empresa.endereco_id).update(
            **{k: form.cleaned_data[k] for k in endereco_keys})

        contato_keys = forms.fields_for_model(Contato, exclude=())
        Contato.objects.filter(pk=empresa.contato_id).update(
            **{k: form.cleaned_data[k] for k in contato_keys})

        return HttpResponseRedirect(self.success_url)

class EmpresaDeleteView(DeleteView):
    model = Empresa
    template_name = 'empresa/delete.html'
    success_url = reverse_lazy('core:empresa_list')
