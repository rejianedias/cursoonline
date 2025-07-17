from django.urls import path
from . import views



urlpatterns = [
    path('', views.catalogo, name='catalogo_cursos'),
    path('<int:curso_id>/modulo/<int:modulo_id>/aula/<int:aula_id>/', views.aula_detalhe, name='aula_detalhe'),
    path('aula/concluir/<int:aula_id>/', views.concluir_aula, name='concluir_aula'),
    path('favoritar/<int:curso_id>/', views.favoritar_curso, name='favoritar_curso'),
    path('quiz/<int:quiz_id>/', views.fazer_quiz, name='fazer_quiz'),
    path('perfil/', views.perfil_aluno, name='perfil_aluno'),
    path('suporte/', views.suporte, name='suporte'),
    path('<int:curso_id>/', views.detalhes_curso, name='detalhes_curso'),
    path('comentario/<int:comentario_id>/deletar/', views.deletar_comentario, name='deletar_comentario'),
    path('comentario/<int:comentario_id>/like/', views.like_comentario, name='like_comentario'),
    path('comentario/<int:comentario_id>/dislike/', views.dislike_comentario, name='dislike_comentario')
]
