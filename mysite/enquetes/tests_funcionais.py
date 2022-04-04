import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from .models import Pergunta


def criar_enquete(texto, qtd_dias):
    """
    Cria uma enquete no banco com o texto e uma quantidade de dias (+/-)
    """
    data = timezone.now() + datetime.timedelta(days=qtd_dias)
    return Pergunta.objects.create(texto=texto, data_publicacao=data)

"""
Testes funcionais de elementos de visão
"""

class IndexViewTests(TestCase):
    def test_sem_nenhuma_enquete_cadastrada(self):
        """
        Caso não existam enquetes cadastradas é exibida uma mensagem específica
        """
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEquals(resposta.status_code, 200)
        self.assertContains(resposta, "Nenhuma enquete cadastrada")
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'], [])

    def test_enquete_no_passado(self):
        """
        Exibidas corretamente enquentes com data de publicação no passado.
        """
        criar_enquete(texto='enquete no passado', qtd_dias=-10)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEquals(resposta.status_code, 200)
        self.assertContains(resposta, "enquete no passado")
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'], ['<Pergunta: enquete no passado>'])

    def test_enquete_no_futuro(self):
        """
        Exibidas com data de publicação no futuro NÃO deve ser exibida
        """
        criar_enquete(texto='enquete no futuro', qtd_dias=1)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEquals(resposta.status_code, 200)
        self.assertContains(resposta, "Nenhuma enquete cadastrada")
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'], [])

    def test_enquete_no_futuro_e_enquete_no_passado(self):
        """
        Exibe a enquete com data no passado e omite a enquete com data no futuro.
        """
        criar_enquete(texto='enquete no passado', qtd_dias=-1)
        criar_enquete(texto='enquete no futuro', qtd_dias=1)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEquals(resposta.status_code, 200)
        self.assertContains(resposta, "enquete no passado")
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'], ['<Pergunta: enquete no passado>'])

    def test_duas_enquetes_no_passado(self):
        criar_enquete(texto='enquete no passado 1', qtd_dias=-5)
        criar_enquete(texto='enquete no passado 2', qtd_dias=-1)
        resposta = self.client.get(reverse('enquetes:index'))
        self.assertEquals(resposta.status_code, 200)
        self.assertContains(resposta, "enquete no passado 1")
        self.assertContains(resposta, "enquete no passado 2")
        self.assertQuerysetEqual(resposta.context['ultimas_enquetes'], ['<Pergunta: enquete no passado 1>', '<Pergunta: enquete no passado 2>'])