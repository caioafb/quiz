import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Pergunta

"""
Testes Unitários de Modelo
"""

class ModelPerguntaTest(TestCase):
    def test_publica_recentemente_com_pergunta_no_futuro(self):
        """ o método publicada_recentemente() deve retornar FALSE quando a pergunta tiver data de publicação futura """
        data_futura = timezone.now() + datetime.timedelta(days=30)
        pergunta_futura = Pergunta(data_publicacao=data_futura)
        self.assertIs(pergunta_futura.publicada_recentemente(), False)

    def test_publica_recentemente_com_pergunta_agora(self):
        """ o método publicada_recentemente() deve retornar TRUE quando a pergunta tiver data de publicação agora """
        data_futura = timezone.now()
        pergunta_agora = Pergunta(data_publicacao=data_futura)
        self.assertIs(pergunta_agora.publicada_recentemente(), True)

    def test_publica_recentemente_com_pergunta_passada(self):
        """ o método publicada_recentemente() deve retornar FALSE quando a pergunta tiver data de publicação além de 24h """
        data_passada = timezone.now() - datetime.timedelta(days = 1, seconds=1)
        pergunta_passada = Pergunta(data_publicacao=data_passada)
        self.assertIs(pergunta_passada.publicada_recentemente(), False)

    def test_publica_recentemente_com_data_dentro_das_ultimas_24h(self):
        """ o método publicada_recentemente() deve retornar TRUE quando a pergunta tiver data de publicação dentro de 24h """
        data = timezone.now() - datetime.timedelta(hours = 23, minutes= 59, seconds=59)
        pergunta = Pergunta(data_publicacao=data)
        self.assertIs(pergunta.publicada_recentemente(), True)