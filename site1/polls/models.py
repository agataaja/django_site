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
