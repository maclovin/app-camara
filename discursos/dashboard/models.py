from django.db import models

# Create your models here.
class Partido(models.Model):
    nome = models.CharField(max_length=256)
    sigla = models.CharField(max_length=8)
    def __unicode__(self):
        return self.sigla

class Estado(models.Model):
    nome = models.CharField(max_length=256)
    sigla = models.CharField(max_length=4)
    def __unicode__(self):
        return self.sigla

class Orador(models.Model):
    nome = models.CharField(max_length=256)
    def __unicode__(self):
        return self.nome

class Discurso(models.Model):
    data = models.DateTimeField()
    discurso = models.TextField()
    sumario = models.TextField()
    fase = models.CharField(max_length=256)
    orador = models.ForeignKey(Orador)
    estado = models.ForeignKey(Estado)
    partido = models.ForeignKey(Partido)
    tags = models.TextField()
    def __unicode__(self):
        return self.orador.nome + ' - ' + self.data.strftime('%d/%m/%Y - %H:%M')

#TODO adicionar suporte a eventos p/ dias
class Evento(models.Model):
    data = models.DateTimeField()
    descricao = models.TextField()
    def __unicode__(self):
        return self.descricao
