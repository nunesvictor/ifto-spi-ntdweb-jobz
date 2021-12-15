from typing import Any, Dict

from core.forms.candidato import CandidatoModelForm
from core.forms.experiencia import ExperienciaModelForm
from core.models import Candidato, Contato, Endereco, ExperienciaProfissional
from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.forms.models import inlineformset_factory, model_to_dict
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


class CandidatoListView(ListView):
    model = Candidato
    template_name = 'candidato/list.html'


class CandidatoCreateView(CreateView):
    form_class = CandidatoModelForm
    template_name = 'candidato/form.html'
    success_url = reverse_lazy('core:candidato_list')
    experiencias_formset = inlineformset_factory(
        Candidato, ExperienciaProfissional, form=ExperienciaModelForm, extra=0, can_delete=False)

    def _create_user(self, form: CandidatoModelForm) -> User:
        user_keys = forms.fields_for_model(
            User, fields=('first_name', 'last_name', 'username',)).keys()
        user_fields = {k: form.cleaned_data[k] for k in user_keys}

        return User.objects.create_user(
            user_fields['username'], **{k: user_fields[k] for k in user_keys if k != 'username'})

    def _create_endereco(self, form: CandidatoModelForm) -> Endereco:
        return Endereco.objects.create(
            **{k: form.cleaned_data[k] for k in forms.fields_for_model(Endereco, exclude=())})

    def _create_contato(self, form: CandidatoModelForm) -> Contato:
        return Contato.objects.create(
            **{k: form.cleaned_data[k] for k in forms.fields_for_model(Contato, exclude=())})

    def _create_candidato(self, form: CandidatoModelForm) -> Candidato:
        candidato = form.save(commit=False)

        candidato.user = self._create_user(form)
        candidato.endereco = self._create_endereco(form)
        candidato.contato = self._create_contato(form)
        candidato.save()

        return candidato

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs.update({'experiencias_formset': self.experiencias_formset()})
        return super().get_context_data(**kwargs)

    @transaction.atomic
    def form_valid(self, form: CandidatoModelForm) -> HttpResponse:
        candidato = self._create_candidato(form)
        experiencias = self.experiencias_formset(form.data, instance=candidato)

        if experiencias.is_valid():
            experiencias.save()
            return HttpResponseRedirect(self.success_url)

        return self.form_invalid(form)


class CandidatoUpdateView(UpdateView):
    model = Candidato
    form_class = CandidatoModelForm
    template_name = 'candidato/form.html'
    success_url = reverse_lazy('core:candidato_list')
    experiencias_formset = inlineformset_factory(
        Candidato, ExperienciaProfissional, form=ExperienciaModelForm, extra=0)

    def _update_user(self, form: CandidatoModelForm) -> None:
        user_keys = forms.fields_for_model(
            User, fields=('first_name', 'last_name', 'username',)).keys()
        user_fields = {k: form.cleaned_data[k] for k in user_keys}
        User.objects.filter(username=user_fields['username']).update(
            **{k: user_fields[k] for k in user_keys})

    def _update_endereco(self, form: CandidatoModelForm, candidato: Candidato) -> None:
        Endereco.objects.filter(pk=candidato.endereco_id).update(
            **{k: form.cleaned_data[k] for k in forms.fields_for_model(Endereco, exclude=())})

    def _update_contato(self, form: CandidatoModelForm, candidato: Candidato) -> None:
        Contato.objects.filter(pk=candidato.contato_id).update(
            **{k: form.cleaned_data[k] for k in forms.fields_for_model(Contato, exclude=())})

    def _update_candidato(self, form: CandidatoModelForm) -> Candidato:
        candidato = form.save()

        self._update_user(form)
        self._update_endereco(form, candidato)
        self._update_contato(form, candidato)

        return candidato

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        kwargs.update(
            {'experiencias_formset': self.experiencias_formset(instance=self.get_object())})
        return super().get_context_data(**kwargs)

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()

        initial.update(model_to_dict(self.get_object().user))
        initial.update(model_to_dict(self.get_object().endereco))
        initial.update(model_to_dict(self.get_object().contato))

        return initial

    @transaction.atomic
    def form_valid(self, form: CandidatoModelForm) -> HttpResponse:
        candidato = self._update_candidato(form)
        experiencias = self.experiencias_formset(form.data, instance=candidato)

        if experiencias.is_valid():
            experiencias.save()
            return HttpResponseRedirect(self.success_url)

        return self.form_invalid(form)


class CandidatoDeleteView(DeleteView):
    model = Candidato
    template_name = 'candidato/delete.html'
    success_url = reverse_lazy('core:candidato_list')
