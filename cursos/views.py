from django.shortcuts import render, get_object_or_404, redirect
from .models import Cursos, Comentario, Aula
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Quiz, Pergunta, Alternativa  as Resposta, ResultadoQuiz
from .models import FAQ
from .forms import DúvidaForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import ComentarioForm 
from django.urls import reverse
from django.http import HttpResponseRedirect




def catalogo(request):
    busca = request.GET.get('busca', '')
    if busca:
        cursos = Cursos.objects.filter(titulo__icontains=busca)
    else:
        cursos = Cursos.objects.all()
    return render(request, 'cursos/catalogo.html', {'cursos': cursos})

from .models import Comentario  
from django.contrib.auth.decorators import login_required

@login_required
def detalhes_curso(request, curso_id):
    curso = get_object_or_404(Cursos, id=curso_id)
    comentarios = curso.comentarios.order_by('-criado_em')

    modulos = list(curso.modulos.order_by('ordem'))
    
    modulos_com_proximo = []
    for i, modulo in enumerate(modulos):
        proximo = modulos[i + 1] if i + 1 < len(modulos) else None
        modulos_com_proximo.append((modulo, proximo))
        
    if request.method == 'POST':
        if 'comentar' in request.POST:
            texto = request.POST.get('comentario')
            if texto:
                Comentario.objects.create(curso=curso, autor=request.user, texto=texto)
            return HttpResponseRedirect(reverse('detalhes_curso', args=[curso.id]) + '#comentarios')

        elif 'favoritar' in request.POST:
            if request.user in curso.alunos_favoritos.all():
                curso.alunos_favoritos.remove(request.user)
            else:
                curso.alunos_favoritos.add(request.user)
            return HttpResponseRedirect(reverse('detalhes_curso', args=[curso.id]) + '#favorito')

    return render(request, 'cursos/detalhes.html', {
        'curso': curso,
        'comentarios': comentarios,
        'modulos_com_proximo': modulos_com_proximo,
    })

    
@login_required
def concluir_aula(request, aula_id):
    aula = get_object_or_404(Aula, id=aula_id)
    aula.concluida_por.add(request.user)
    return redirect('detalhes_curso', curso_id=aula.modulo.curso.id)

@login_required
def favoritar_curso(request, curso_id):
    curso = get_object_or_404(Cursos, id=curso_id)
    if request.user in curso.alunos_favoritos.all():
        curso.alunos_favoritos.remove(request.user)
    else:
        curso.alunos_favoritos.add(request.user)
    return HttpResponseRedirect(
    reverse('detalhes_curso', args=[curso_id]) + '#favorito'
)


@login_required
def aula_detalhe(request, curso_id, modulo_id, aula_id):
    aula = get_object_or_404(Aula, id=aula_id, modulo__id=modulo_id, modulo__curso__id=curso_id)
    comentarios = aula.comentarios.order_by('-criado_em')

    if request.method == 'POST':
        if 'concluir' in request.POST:
            aula.concluida_por.add(request.user)
            return redirect(request.path)

        elif 'comentar' in request.POST:
            texto = request.POST.get('comentario')
            if texto:
                Comentario.objects.create(aula=aula, autor=request.user, texto=texto)
                return HttpResponseRedirect(
                    reverse('aula_detalhe', args=[curso_id, modulo_id, aula_id]) + '#comentarios'
                )

    proximas = Aula.objects.filter(modulo_id=modulo_id, id__gt=aula.id).order_by('id')
    proxima_aula = proximas.first() if proximas.exists() else None

    return render(request, 'cursos/aula_detalhe.html', {
        'aula': aula,
        'comentarios': comentarios,
        'proxima_aula': proxima_aula,
        'modulo': aula.modulo,
    })

@login_required
def like_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user in comentario.dislikes.all():
        comentario.dislikes.remove(request.user)
    if request.user in comentario.likes.all():
        comentario.likes.remove(request.user)
    else:
        comentario.likes.add(request.user)

    if comentario.aula:  # redirecionar para a aula
        return redirect('aula_detalhe', curso_id=comentario.aula.modulo.curso.id,
                        modulo_id=comentario.aula.modulo.id,
                        aula_id=comentario.aula.id)
    else:  # redirecionar para o curso
        return redirect('detalhes_curso', curso_id=comentario.curso.id)


@login_required
def dislike_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if request.user in comentario.likes.all():
        comentario.likes.remove(request.user)
    if request.user in comentario.dislikes.all():
        comentario.dislikes.remove(request.user)
    else:
        comentario.dislikes.add(request.user)

    if comentario.aula:
        return redirect('aula_detalhe', curso_id=comentario.aula.modulo.curso.id,
                        modulo_id=comentario.aula.modulo.id,
                        aula_id=comentario.aula.id)
    else:
        return redirect('detalhes_curso', curso_id=comentario.curso.id)


@login_required
def deletar_comentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if comentario.autor != request.user:
        return redirect('home')  # ou mostrar erro

    if comentario.aula:
        curso_id = comentario.aula.modulo.curso.id
        modulo_id = comentario.aula.modulo.id
        aula_id = comentario.aula.id
        comentario.delete()
        return redirect('aula_detalhe', curso_id=curso_id, modulo_id=modulo_id, aula_id=aula_id)
    else:
        curso_id = comentario.curso.id
        comentario.delete()
        return redirect('detalhes_curso', curso_id=curso_id)


#parte do quiz



@login_required
def fazer_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    perguntas = quiz.perguntas.all()

    if request.method == 'POST':
        pontuacao = 0
        for pergunta in perguntas:
            resposta_id = request.POST.get(str(pergunta.id))
            if resposta_id:
                resposta = Resposta.objects.get(id=int(resposta_id))
                if resposta.correta:
                    pontuacao += 1
        ResultadoQuiz.objects.create(aluno=request.user, quiz=quiz, pontuacao=pontuacao)
        return render(request, 'cursos/resultado_quiz.html', {
            'pontuacao': pontuacao,
            'total': perguntas.count(),
        })

# perfil do aluno


@login_required
def perfil_aluno(request):
    favoritos = request.user.cursos_favoritos.all()
    concluidas = request.user.aulas_concluidas.all()
    return render(request, 'curso/perfil.html', {
        'favoritos': favoritos,
        'aulas_concluidas': concluidas,
    })

# views para suporte

def suporte(request):
    faqs = FAQ.objects.all()
    enviado = False

    if request.method == 'POST':
        form = DúvidaForm(request.POST)
        if form.is_valid():
            assunto = form.cleaned_data['assunto']
            mensagem = form.cleaned_data['mensagem']
            send_mail(
                f"[DÚVIDA] {assunto}",
                mensagem,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # ou email de suporte
            )
            enviado = True
    else:
        form = DúvidaForm()

    return render(request, 'curso/suporte.html', {
        'faqs': faqs,
        'form': form,
        'enviado': enviado,
    })


def home(request):
    return render(request,'cursos/home.html')