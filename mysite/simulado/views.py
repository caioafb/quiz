from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Rotulo, Usuario, Questao, Alternativa, Simulado, Resultado

class IndexView(generic.View):
    def get(self, request, *args, **kwargs):
        simulados = Simulado.objects.all().order_by('-data_publicacao')
        resultados = Resultado.objects.all().order_by('-data_publicacao')[:10]
        contexto = {
            'simulados':simulados,
            'resultados':resultados
        }
        return render(request, 'simulado/index.html', contexto)

@method_decorator(login_required, name='dispatch')
class SimuladoView(generic.View):
    def get(self, request, *args, **kwargs):
        simulado_id = kwargs['pk']
        simulado = Simulado.objects.get(pk=simulado_id)
        contexto = {
            'simulado':simulado
        }
        return render(request, 'simulado/simulado.html', contexto)

    def post(self, request, *args, **kwargs):
        simulado_id = kwargs['pk']
        simulado = Simulado.objects.get(pk=simulado_id)
        usuario = request.user.usuario
        cont = 0
        pontuacao_maxima = 0
        pontuacao = 0
        respostas = []
        for field in request.POST:
            if cont > 0:
                chave = request.POST[field]
                alternativa = Alternativa.objects.get(pk=chave)
                respostas.append(alternativa.id)
                pontuacao_maxima = pontuacao_maxima + alternativa.questao.pontuacao
                if alternativa.correta:
                    pontuacao = pontuacao + alternativa.questao.pontuacao
            cont = cont + 1

        resultado = (10 * pontuacao)/pontuacao_maxima
        nota = Resultado(nota = resultado, simulado = simulado, usuario = usuario, data_publicacao = timezone.now())
        nota.save()

        contexto = {
            'resultado':resultado,
            'respostas':respostas,
            'simulado':simulado
        }

        return render(request, 'simulado/resultado.html', contexto)

class PerfilView(generic.View):
    def get(self, request, *args, **kwargs):
        usuario = request.user.usuario
        contexto = {
            'usuario':usuario
        }
        return render(request, 'simulado/perfil.html', contexto)


class NovoSimuladoView(generic.View):
    def get(self, request, *args, **kwargs):
        temas = Rotulo.objects.all().order_by("tema")
        contexto = {
            'temas':temas
        }
        return render(request, 'simulado/novo_simulado.html', contexto)
    def post(self, request, *args, **kwargs):
        texto = request.POST['texto']
        usuario = request.user.usuario

        if Simulado.objects.filter(titulo=texto).exists():
            return render(request, 'simulado/index.html', {'erro': 'Simulado com mesmo título já cadastrado.'})

        simulado = Simulado(titulo=texto, data_publicacao = timezone.now(), autor=usuario)
        simulado.save()

        cont = 0
        for field in request.POST:
            if cont > 1:
                questao = Questao.objects.get(pk=field)
                if questao:
                    simulado.questao.add(questao)
            cont = cont + 1
        simulado.save()
        simulados = Simulado.objects.all().order_by('-data_publicacao')
        contexto = {
            'simulados':simulados,
            'msg': 'Simulado cadastrado com sucesso!'
        }
        return render(request, 'simulado/index.html', contexto)

class NovaQuestaoView(generic.View):
    def get(self, request, *args, **kwargs):
        temas = Rotulo.objects.all().order_by("tema")
        contexto = {
            'temas': temas
        }
        return render(request, 'simulado/nova_questao.html', contexto)

    def post(self, request, *args, **kwargs):
        texto = request.POST['texto']
        alt1 = request.POST['alt1']
        alt2 = request.POST['alt2']
        alt3 = request.POST['alt3']
        alt4 = request.POST['alt4']
        alt5 = request.POST['alt5']
        score = request.POST['score']
        resposta = request.POST['correta']
        temaid = request.POST['tema']
        usuario = request.user.usuario

        if Questao.objects.filter(texto=texto).exists():
            return render(request, 'simulado/index.html', {'erro': 'Questão com o mesmo texto já cadastrada.'})

        if temaid:
            tema = Rotulo.objects.get(pk=temaid)
        else:
            return render(request, 'simulado/nova_questao.html', {'erro': 'Um tema deve ser selecionado.'})

        if not resposta:
            return render(request, 'simulado/nova_questao.html', {'erro': 'Uma alternativa deve ser correta.'})

        questao = Questao(texto=texto, data_publicacao = timezone.now(), rotulo=tema, autor=usuario, pontuacao=score)
        alternativa1 = Alternativa(texto = alt1, questao = questao)
        alternativa2 = Alternativa(texto = alt2, questao = questao)
        questao.save()
        alternativa1.save()
        alternativa2.save()
        if alt3:
            alternativa3 = Alternativa(texto = alt3, questao = questao)
            alternativa3.save()
        if alt4:
            alternativa4 = Alternativa(texto = alt4, questao = questao)
            alternativa4.save()
        if alt5:
            alternativa5 = Alternativa(texto = alt5, questao = questao)
            alternativa5.save()

        if resposta == "1":
            alternativa1.correta = True
            alternativa1.save()
        elif resposta == "2":
            alternativa2.correta = True
            alternativa2.save()
        elif resposta == "3":
            alternativa3.correta = True
            alternativa3.save()
        elif resposta == "4":
            alternativa4.correta = True
            alternativa4.save()
        elif resposta == "5":
            alternativa5.correta = True
            alternativa5.save()

        temas = Rotulo.objects.all().order_by("tema")
        contexto = {
            'temas': temas,
            'msg': 'Questão cadastrada com sucesso!'
        }
        return render(request, 'simulado/nova_questao.html', contexto)

class NovoTemaView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'simulado/novo_tema.html')

    def post(self, request, *args, **kwargs):
        tema = request.POST['tema']
        if not Rotulo.objects.filter(tema=tema).exists():
            tema = Rotulo(tema=tema)
            tema.save()
        else:
            return render(request, 'simulado/novo_tema.html', {'erro': 'Tema já cadastrado.'})
        temas = Rotulo.objects.all().order_by("tema")
        contexto = {
            'temas': temas
        }
        return render(request, 'simulado/nova_questao.html', contexto)

class NovoUsuarioView(generic.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'simulado/novo_usuario.html')

    def post(self, request, *args, **kwargs):
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        email = request.POST['email']
        username = request.POST['login']
        senha1 = request.POST['senha1']
        senha2 = request.POST['senha2']

        simulados = Simulado.objects.all().order_by('-data_publicacao')
        resultados = Resultado.objects.all().order_by('-data_publicacao')[:10]
        contexto = {
            'simulados':simulados,
            'resultados':resultados,
            'msg':'Usuário cadastrado com sucesso!'
        }

        if (nome and sobrenome and email and username and senha1 and senha2):
            if senha1 == senha2:
                if not User.objects.filter(username=username).exists():
                    if not User.objects.filter(email=email).exists():
                        user = User.objects.create_user(username, email, senha1)
                        user.first_name = nome
                        user.last_name = sobrenome
                        user.save()
                        usuario = Usuario(nome = nome, user = user)
                        usuario.save()
                    else:
                        return render(request, 'simulado/novo_usuario.html', {'erro': 'E-mail informado já existente.'})
                else:
                    return render(request, 'simulado/novo_usuario.html', {'erro': 'Login informado já existente.'})
            else:
                return render(request, 'simulado/novo_usuario.html', {'erro': 'Senha informadas diferentes.'})
        else:
            return render(request, 'simulado/novo_usuario.html', {'erro': 'Todos os parâmetros devem ser preenchidos.'})
        login(request, user)
        return render(request, 'simulado/index.html', contexto)





