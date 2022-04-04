from django.db import models
from django.conf import settings

class Rotulo(models.Model):
    tema = models.CharField(max_length=20)
    def questoes(self):
        return Questao.objects.filter(rotulo=self)
    def __str__(self):
        return self.tema

class Usuario(models.Model):
    nome = models.CharField(max_length=80)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def resultados(self):
        return Resultado.objects.filter(usuario=self)
    def __str__(self):
        return self.nome

class Questao(models.Model):
    texto = models.CharField(max_length=200, unique=True)
    data_publicacao = models.DateTimeField('Data de publicação')
    rotulo = models.ForeignKey(Rotulo, on_delete=models.DO_NOTHING)
    autor = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    pontuacao = models.IntegerField()
    class Meta:
        verbose_name_plural = "Questoes"
    def alternativas(self):
        return Alternativa.objects.filter(questao=self)
    def __str__(self):
        return self.texto

class Simulado(models.Model):
    titulo = models.CharField(max_length=200, unique=True)
    data_publicacao = models.DateTimeField('Data de publicação')
    autor = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    questao = models.ManyToManyField(Questao, blank=True, null=True, related_name='simulado')
    def questoes(self):
        return Questao.objects.filter(simulado=self)
    def __str__(self):
        return self.titulo

class Alternativa(models.Model):
    texto = models.CharField(max_length=100)
    correta = models.BooleanField(default = False)
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    def __str__(self):
        return self.texto

class Resultado(models.Model):
    nota = models.FloatField()
    simulado = models.ForeignKey(Simulado, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    data_publicacao = models.DateTimeField('Data de publicação')
    def __str__(self):
        return self.usuario