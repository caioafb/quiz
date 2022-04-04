from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from .models import Pergunta, Opcao


class IndexView(generic.View):
    def get (self, request, *args, **kwargs):
        ultimas_enquetes = Pergunta.objects.filter(data_publicacao__lte=timezone.now()).order_by('data_publicacao')[:100]
        contexto = {
            'ultimas_enquetes': ultimas_enquetes,
        }
        return render(request, 'enquetes/index.html', contexto)

class BuscaView(generic.View):
    def get (self, request, *args, **kwargs):
        str_busca = request.GET['str_busca']
        enquetes = Pergunta.objects.filter(
            data_publicacao__lte=timezone.now()
        ).filter(
            data_encerramento__gt = timezone.now()
        ).order_by('-data_publicacao')
        if str_busca:
            enquetes = enquetes.filter(texto__icontains = str_busca)
        contexto = {
            'enquetes': enquetes,
        }
        return render(request, 'enquetes/busca.html', contexto)

class DetalhesView(generic.View):
    def get(self, request, *args, **kwargs):
        id_enquete = kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk=id_enquete)
        return render(request, 'enquetes/detalhes.html', {'pergunta':pergunta})

class VotacaoView(generic.View):
    def post(self, request, *args, **kwargs):
        id_enquete = kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk=id_enquete)
        try:
            op_selecionada = pergunta.opcao_set.get(pk=request.POST['opcao'])
        except (KeyError, Opcao.DoesNotExist):
            return render(request, 'enquetes/detalhes.html', {
                'pergunta': pergunta,
                'erro': "Uma opção precisa ser selecionada!",
            })
        else:
            op_selecionada.votos += 1
            op_selecionada.save()
        return HttpResponseRedirect(reverse('enquetes:resultado', args=(pergunta.id,)))

class ResultadoView(generic.View):
    def get (self, request, *args, **kwargs):
        id_enquete = kwargs['pk']
        pergunta = get_object_or_404(Pergunta, pk=id_enquete)
        return render(request, 'enquetes/resultado.html', {'pergunta':pergunta})

@method_decorator(login_required, name='dispatch')
class CadastroView(generic.View):
    def get (self, request, *args, **kwargs):
        return render(request, 'enquetes/cadastro.html')

    def post(self, request, *args, **kwargs):
        texto = request.POST['texto']
        op1 = request.POST['op1']
        op2 = request.POST['op2']
        op3 = request.POST['op3']
        op4 = request.POST['op4']
        op5 = request.POST['op5']
        op6 = request.POST['op6']
        if texto and op1 and op2:
            p1 = Pergunta(texto=texto, data_publicacao = timezone.now())
            opcao1 = Opcao(texto = op1, pergunta = p1)
            opcao2 = Opcao(texto = op2, pergunta = p1)
            p1.save()
            opcao1.save()
            opcao2.save()
            if op3:
                opcao3 = Opcao(texto = op3, pergunta = p1)
                opcao3.save()
            if op4:
                opcao4 = Opcao(texto = op4, pergunta = p1)
                opcao4.save()
            if op5:
                opcao5 = Opcao(texto = op5, pergunta = p1)
                opcao5.save()
            if op6:
                opcao6 = Opcao(texto = op6, pergunta = p1)
                opcao6.save()
        else:
            return render(request, 'enquetes/cadastro.html', {'erro': 'Precisa preencher pelo menos o texto e duas opções.'})
        return HttpResponseRedirect(reverse('enquetes:index', args=()))






"""
############### Elementos de View enquanto FUNÇÕES ###############

def index(request):
    ultimas_enquetes = Pergunta.objects.order_by('data_publicacao')[:6]
    contexto = {
        'ultimas_enquetes': ultimas_enquetes,
    }
    return render(request, 'enquetes/index.html', contexto)

def detalhes(request, id_enquete):
    pergunta = get_object_or_404(Pergunta, pk=id_enquete)
    return render(request, 'enquetes/detalhes.html', {'pergunta':pergunta})

def resultado(request, id_enquete):
    pergunta = get_object_or_404(Pergunta, pk=id_enquete)
    return render(request, 'enquetes/resultado.html', {'pergunta': pergunta})

def votacao(request, id_enquete):
    pergunta = get_object_or_404(Pergunta, pk=id_enquete)
    try:
        op_selecionada = pergunta.opcao_set.get(pk=request.POST['opcao'])
    except (KeyError, Opcao.DoesNotExist):
        return render(request, 'enquetes/detalhes.html', {
            'pergunta': pergunta,
            'error_message': "Uma opção precisa ser selecionada!",
            })
    else:
        op_selecionada.votos += 1
        op_selecionada.save()
    return HttpResponseRedirect(reverse('enquetes:resultado', args=(pergunta.id,)))

##################################################################

###### Elementos de View enquanto Classes de View Genéricas ######

class IndexView(generic.ListView):
    template_name = 'enquetes/index.html'
    context_object_name = 'ultimas_enquetes'
    def get_queryset(self):
        return Pergunta.objects.order_by('data_publicacao')[:6]

class DetalhesView(generic.DetailView):
    model = Pergunta
    template_name = 'enquetes/detalhes.html'

class ResultadoView(generic.DetailView):
    model = Pergunta
    template_name = 'enquetes/resultado.html'
"""


