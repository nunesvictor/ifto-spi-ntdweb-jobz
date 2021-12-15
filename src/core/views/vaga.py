from django.urls import reverse_lazy
from core.forms.vaga import VagaModelForm
from core.models import Vaga
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView


class VagaListView(ListView):
    model = Vaga
    template_name = 'vaga/list.html'


class VagaCreateView(CreateView):
    form_class = VagaModelForm
    template_name = 'vaga/form.html'
    success_url = reverse_lazy('core:vaga_list')


class VagaUpdateView(UpdateView):
    model = Vaga
    form_class = VagaModelForm
    template_name = 'vaga/form.html'
    success_url = reverse_lazy('core:vaga_list')


class VagaDeleteView(DeleteView):
    model = Vaga
    template_name = 'vaga/delete.html'
    success_url = reverse_lazy('core:vaga_list')
