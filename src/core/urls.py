from django.urls import path

from .views.candidato import (
    CandidatoCreateView,
    CandidatoDeleteView,
    CandidatoListView,
    CandidatoUpdateView,
)
from .views.empresa import (
    EmpresaCreateView,
    EmpresaDeleteView,
    EmpresaListView,
    EmpresaUpdateView,
)
from .views.vaga import (
    VagaCreateView,
    VagaDeleteView,
    VagaListView,
    VagaUpdateView,
)

app_name = 'core'

urlpatterns = [
    path('candidatos/', CandidatoListView.as_view(), name="candidato_list"),
    path('candidatos/add', CandidatoCreateView.as_view(), name="candidato_add"),
    path('candidatos/<int:pk>/edit',
         CandidatoUpdateView.as_view(), name="candidato_edit"),
    path('candidatos/<int:pk>/delete',
         CandidatoDeleteView.as_view(), name="candidato_delete"),

    path('empresas/', EmpresaListView.as_view(), name="empresa_list"),
    path('empresas/add', EmpresaCreateView.as_view(), name="empresa_add"),
    path('empresas/<int:pk>/edit', EmpresaUpdateView.as_view(), name="empresa_edit"),
    path('empresas/<int:pk>/delete',
         EmpresaDeleteView.as_view(), name="empresa_delete"),

    path('vagas/', VagaListView.as_view(), name="vaga_list"),
    path('vagas/add', VagaCreateView.as_view(), name="vaga_add"),
    path('vagas/<int:pk>/edit', VagaUpdateView.as_view(), name="vaga_edit"),
    path('vagas/<int:pk>/delete',
         VagaDeleteView.as_view(), name="vaga_delete"),
]
