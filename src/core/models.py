from typing import Union

from core.mask_utils import mask_cep
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet


class UF(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    sigla = models.CharField(max_length=2)

    class Meta:
        verbose_name = 'unidade federativa'
        verbose_name_plural = 'unidades federativas'
        ordering = 'nome',

    def __str__(self) -> str:
        return self.nome


class Genero(models.Model):
    descricao = models.CharField('descrição', max_length=50, unique=True)

    class Meta:
        verbose_name = 'gênero'
        ordering = 'pk',

    def __str__(self) -> str:
        return self.descricao


class EstadoCivil(models.Model):
    descricao = models.CharField('descrição', max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'estados civis'
        ordering = 'pk',

    def __str__(self) -> str:
        return self.descricao


class Endereco(models.Model):
    logradouro = models.CharField(max_length=200)
    tipo_logradouro = models.CharField('tipo de logradouro', max_length=50)
    bairroDistrito = models.CharField('bairro ou distrito', max_length=200)
    uf = models.ForeignKey(UF, verbose_name='UF', on_delete=models.CASCADE)
    localidade = models.CharField(max_length=200)
    cep = models.CharField(verbose_name='CEP', max_length=8)

    class Meta:
        verbose_name = 'endereço'

    def __str__(self) -> str:
        return "{} {}. {}. {}-{}. CEP: {}".format(
            self.tipo_logradouro,
            self.logradouro,
            self.bairroDistrito,
            self.localidade,
            self.uf.sigla,
            mask_cep(self.cep))


class Contato(models.Model):
    email = models.CharField('e-mail', max_length=100, unique=True)
    telefone = models.CharField(max_length=11)
    fax = models.CharField(max_length=11, blank=True, null=True)
    newsletter_subscriber = models.BooleanField(
        'inscrever na newsletter', default=False)

    def __str__(self) -> str:
        return self.telefone


class AreaAtuacao(models.Model):
    descricao = models.CharField('descrição', max_length=50, unique=True)

    class Meta:
        verbose_name = 'área de atuação'
        verbose_name_plural = 'áreas de atuação'

    def __str__(self) -> str:
        return self.descricao


class Empresa(models.Model):
    user = models.ForeignKey(
        User, verbose_name='usuário', on_delete=models.CASCADE)
    razao_social = models.CharField('razão social', max_length=200)
    cnpj = models.CharField('CNPJ', max_length=14, unique=True)
    area_atuacao = models.ForeignKey(
        AreaAtuacao, verbose_name='área de atuação', on_delete=models.CASCADE)
    endereco = models.ForeignKey(
        Endereco, verbose_name='endereço', on_delete=models.CASCADE)
    contato = models.ForeignKey(
        Contato, verbose_name='contato', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.razao_social


class Cargo(models.Model):
    descricao = models.CharField('descrição', max_length=50, unique=True)
    especificacoes = models.TextField('especificações')

    def __str__(self) -> str:
        return self.descricao


class FormaContratacao(models.Model):
    descricao = models.CharField('descrição', max_length=50, unique=True)

    class Meta:
        verbose_name = 'forma de contratação'
        verbose_name_plural = 'formas de contratação'
        ordering = 'pk',

    def __str__(self) -> str:
        return self.descricao


class CandidatoQuerySet(QuerySet['Candidato']):
    def por_cargo(self, q: Union[str, Cargo]) -> QuerySet['Candidato']:
        fields = ('vaga__cargo__descricao', 'vaga__cargo__especificacoes',)

        if type(q) == str:
            options = Q()

            for field in fields:
                options |= Q(**{field + '__icontains': q})

            return self.filter(options)
        elif type(q) == Cargo:
            return self.filter(vaga__cargo=q)

        return self

    def por_localidade(self, q: str) -> QuerySet['Candidato']:
        return self.filter(vaga__localidade__icontains=q)

    def por_uf(self, q) -> QuerySet['Candidato']:
        fields = ('vaga__uf__nome', 'vaga__uf__sigla',)

        if q:
            options = Q()

            for field in fields:
                options |= Q(**{field + '__icontains': q})

            return self.filter(options)

        return self


class Candidato(models.Model):
    user = models.ForeignKey(
        User, verbose_name='usuário', on_delete=models.CASCADE)
    cpf = models.CharField('CPF', max_length=11)
    rg = models.CharField('RG', max_length=50)
    orgao_expedidor = models.CharField('órgão expedidor', max_length=50)
    uf_expedicao = models.ForeignKey(
        UF, verbose_name='UF de expedição', on_delete=models.CASCADE)
    data_expedicao = models.DateField('data de expedição')
    genero = models.ForeignKey(
        Genero, verbose_name='gênero', on_delete=models.CASCADE)
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.CASCADE)
    endereco = models.ForeignKey(
        Endereco, verbose_name='endereço', on_delete=models.CASCADE)
    contato = models.ForeignKey(
        Contato, verbose_name='contato', on_delete=models.CASCADE)
    objects = CandidatoQuerySet.as_manager()

    def __str__(self) -> str:
        return '{} {}'.format(self.user.first_name, self.user.last_name)


class ExperienciaProfissional(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    tarefas_executadas = models.TextField('tarefas executadas')
    forma_contratacao = models.ForeignKey(
        FormaContratacao, verbose_name='forma de contratação', on_delete=models.CASCADE)
    data_inicio = models.DateField('data de início')
    data_conclusao = models.DateField(
        'data de conclusão', blank=True, null=True)

    class Meta:
        verbose_name = 'experiência profissinal'
        verbose_name_plural = 'experiências profissionais'

    def __str__(self) -> str:
        return "{} ({} - {})".format(
            self.empresa, self.data_inicio, self.data_conclusao)


class Turno(models.Model):
    descricao = models.CharField('descrição', max_length=50, unique=True)

    class Meta:
        ordering = 'pk',

    def __str__(self) -> str:
        return self.descricao


class VagaQuerySet(QuerySet['Vaga']):
    def por_empresa(self, q: Union[str, Empresa]) -> QuerySet['Vaga']:
        fields = ('empresa__razao_social', 'empresa__cnpj',)

        if type(q) == str:
            options = Q()

            for field in fields:
                options |= Q(**{field + '__icontains': q})

            return self.filter(options)
        elif type(q) == Empresa:
            return self.filter(empresa=q)

        return self

    def por_cargo(self, q: Union[str, Cargo]) -> QuerySet['Vaga']:
        fields = ('cargo__descricao', 'cargo__especificacoes',)

        if type(q) == str:
            options = Q()

            for field in fields:
                options |= Q(**{field + '__icontains': q})

            return self.filter(options)
        elif type(q) == Cargo:
            return self.filter(cargo=q)

        return self

    def por_localidade(self, q: str) -> QuerySet['Vaga']:
        return self.filter(localidade__icontains=q)

    def por_uf(self, q: str) -> QuerySet['Vaga']:
        fields = ('uf__nome', 'uf__sigla',)
        options = Q()

        for field in fields:
            options |= Q(**{field + '__icontains': q})

        return self.filter(options)


class Vaga(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    remuneracao = models.DecimalField(
        'remuneração', decimal_places=2, max_digits=8)
    vale_transporte = models.BooleanField('vale transporte', default=False)
    vale_refeicao = models.BooleanField('vale refeição', default=False)
    outros = models.TextField()
    turno = models.ForeignKey(Turno, on_delete=models.CASCADE)
    forma_contratacao = models.ForeignKey(
        FormaContratacao, verbose_name='forma de contratação', on_delete=models.CASCADE)
    localidade = models.CharField(max_length=200)
    uf = models.ForeignKey(UF, verbose_name='UF', on_delete=models.CASCADE)
    candidatos = models.ManyToManyField(Candidato, blank=True)
    objects = VagaQuerySet.as_manager()

    def __str__(self) -> str:
        return "{}. ({})".format(self.cargo, self.remuneracao)
