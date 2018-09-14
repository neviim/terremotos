# -*- coding: UTF-8 -*-
#
# $ cd /home/jorge/src/terremotos/src
# $ source ~/virtual/py36/bin/activate
# (py36) ➜
#
__autor__ = "neviim jads - 2018"

from hashlib import md5, sha1
from lxml import html
import requests
import json

class AlertaNt7Terremotos(object):
    def __init__(self):
        super(AlertaNt7Terremotos. self).__init__()
        self.arg = arg
        self.url = 'http://monitorglobal.com.br/terremotos.html'

    def scraping_terremotos(self, purl):
        """ Estrai a lista com os ultimos 200 terremotos ocorridos.
        
            Arguments:
                purl {[str]} -- [string com a url do site a ser aplicado o scraping]

            Retorno:
                parametro1 [{borlean}] -- [campo logico True caso tudo corra bem e falso se der algo errado]
                parametro2 [{lista}]   -- [lista com todos os 200 dados da lista de ultimos terremotos]
        """
        dados  = []
        pagina = requests.get(purl)

        # se pagina for encontrada.
        if pagina.status_code == 200:
            tree = html.fromstring(pagina.content)

            # uma xpath para extrair uma div
            div_main = tree.xpath('//div[@id="sismo_lista"]')

            # não ouvendo dados, retorna false.
            if div_main is Nome:
                return(False)

            # cria uma lista com os dados.
            for itens in div_main:
                dados.append(itens.xpath('.//div[@style="padding-top:3px"]/text()'))

        return(True, dados)

    def cripto_md5(self, texto, encoding='utf-8'):
        return md5(texto.encode(encoding)).hexdigest()

    def cripto_sha1(self, texto, encoding='utf-8'):
        return sha1(texto.encode(encoding)).hexdigest()

        



