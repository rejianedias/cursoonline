from django.db import models
from accounts.models import CustomUser
from cursos.models import Cursos

 #class Quiz(models.Model):
    #curso = models.ForeignKey(Cursos, on_delete=models.CASCADE, related_name='quizzes')
    #itulo = models.CharField(max_length=100)

    #def __str__(self):
     #   return self.titulo

class Pergunta(models.Model):
    quiz = models.ForeignKey(Cursos, on_delete=models.CASCADE, related_name='perguntas')
    texto = models.TextField()

    def __str__(self):
        return self.texto

class Alternativa(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='alternativas')
    texto = models.CharField(max_length=200)
    correta = models.BooleanField(default=False)

    def __str__(self):
        return self.texto

#class ResultadoQuiz(models.Model):
 #   aluno = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  #  quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
   # pontuacao = models.FloatField()
    #data = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
     #   return f"{self.aluno.username} - {self.quiz.titulo}"


# Create your models here.
