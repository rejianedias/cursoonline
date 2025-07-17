from django.db import models
from accounts.models import CustomUser
from django.contrib.auth import get_user_model  #perfil do aluno
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

User = get_user_model()  # perfil do aluno


class Cursos(models.Model):
    titulo = models.CharField(max_length=200) 
    descricao = models.TextField()
    professor = models.CharField(max_length=100)
    imagem = models.ImageField(upload_to='cursos/', null=True, blank=True)
    url_video = models.URLField()
    materiais = models.FileField(upload_to='materiais/', null=True, blank=True)
    alunos_favoritos = models.ManyToManyField(CustomUser, blank=True, related_name='favoritos')
    

    def __str__(self):
        return self.titulo
    

class Module(models.Model):
    curso = models.ForeignKey(Cursos, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    ordem = models.PositiveIntegerField(default=0)
class Meta:
    ordering = ['ordem']

    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"
    
    
class Aula(models.Model):
    modulo = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='aulas')
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    video_id = models.CharField("ID do vídeo no YouTube", max_length=20, blank=True)

   
    concluida_por = models.ManyToManyField(
        CustomUser,  # ou 'accounts.CustomUser'
        related_name='aulas_concluidas',
        blank=True
    )    
    def __str__(self):
        return self.titulo
    def clean(self):
        if self.titulo.strip().lower() == "meta viewport":
            raise ValidationError({'titulo': "Esse título não é permitido."})
    

class Comentario(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    criado_em = models.DateTimeField(auto_now_add=True)

    curso = models.ForeignKey('Cursos', on_delete=models.CASCADE, null=True, blank=True, related_name='comentarios')
    aula = models.ForeignKey('Aula', on_delete=models.CASCADE, null=True, blank=True, related_name='comentarios')

    likes = models.ManyToManyField(User, related_name='comentarios_curtidos', blank=True)
    dislikes = models.ManyToManyField(User, related_name='comentarios_descurtidos', blank=True)

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return f"Comentário de {self.autor.username} - {self.texto[:30]}"


#parte do quiz sendo iniciada!
class Quiz(models.Model):
    curso = models.ForeignKey(Cursos, on_delete=models.CASCADE, related_name='quizzes')
    titulo = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo


class Pergunta(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='perguntas')
    texto = models.TextField()

    def __str__(self):
        return self.texto


class Alternativa(models.Model):
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='alternativas')
    texto = models.CharField(max_length=300)
    correta = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.texto} ({'Correta' if self.correta else 'Errada'})"


class ResultadoQuiz(models.Model):
    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    pontuacao = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.aluno.username} - {self.quiz.titulo} ({self.pontuacao} pts)"


# FAQ
class FAQ(models.Model):
    pergunta = models.CharField(max_length=200)
    resposta = models.TextField()

    def __str__(self):
        return self.pergunta


# Comentário da aula
#class Comentariodaaula(models.Model):
    #aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name='comentarios')
    #autor = models.ForeignKey(User, on_delete=models.CASCADE)
    #texto = models.TextField()
    #criado_em = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
       # return f"Comentário de {self.autor.username} em {self.aula.titulo}"