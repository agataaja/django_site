from django.db import models

# Create your models here.


# Questão - texto com 200 caracteres + data da publicação

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


# Escolha - Toda alternativa vai estar vinculada a uma pergunta

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Caso apague a pergunta as escolhas também serão apagas
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class WebhookPayload(models.Model):

    received_at = models.DateTimeField(auto_now_add=True)
    payload = models.JSONField()


class Luta(models.Model):

    id = models.CharField(max_length=50, primary_key=True)  # UUID + id_evento
    id_evento = models.IntegerField()
    id_atleta1 = models.IntegerField()
    id_atleta2 = models.IntegerField()
    flag_finalizado = models.BooleanField()
    round = models.CharField(max_length=150)
    id_atleta_ganhador = models.IntegerField(null=True, blank=True)
    sportAlternateName = models.CharField(max_length=150)
    weightCategoryName = models.CharField(max_length=150)
    audienceName = models.CharField(max_length=150)
    id_classe_peso = models.IntegerField(null=True, blank=True)

    atleta1_flag_injured = models.BooleanField(null=True, blank=True)
    atleta1_flag_seeded = models.BooleanField(null=True, blank=True)
    atleta1_draw_rank = models.CharField(max_length=10, null=True, blank=True)
    atleta1_RobinRank = models.CharField(max_length=10, null=True, blank=True)

    atleta2_flag_injured = models.BooleanField(null=True, blank=True)
    atleta2_flag_seeded = models.BooleanField(null=True, blank=True)
    atleta2_draw_rank = models.CharField(max_length=10, null=True, blank=True)
    atleta2_RobinRank = models.CharField(max_length=10, null=True, blank=True)

    resultado = models.CharField(max_length=30, null=True, blank=True)
    tipo_vitoria = models.CharField(max_length=10, null=True, blank=True)

    atleta1_ranking_point = models.IntegerField(null=True, blank=True)
    atleta2_ranking_point = models.IntegerField(null=True, blank=True)

    numero = models.IntegerField(null=True, blank=True)
    tapete = models.CharField(max_length=10)

    data_inicio = models.DateTimeField(null=True, blank=True)
    data_fim = models.DateTimeField(null=True, blank=True)
