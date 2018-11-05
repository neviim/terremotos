# -*- coding: UTF-8 -*-
#
#   Ambiente de desemvolvimento:
#       
#       Dados dos ultimos registros de terremotos no mundo.
#           
#           url: http://monitorglobal.com.br/terremotos.html
#
#       Referencia: 
#
#       $ conda activate D:\__CondaVirtual\pytr37
#       $ code .
#       $ conda deactivate
#
#       $ conda create --prefix C:\path_do_projeto\py37\ python=3.7
#       $ conda deactivate
#
#       $ cd C:\Users\jorge.FCN\Documents\GitHub\_python_projetos
#       $ cd /home/jorge/src/terremotos/src
#       $ source ~/virtual/py36/bin/activate
#
#       (py36-tr) ➜ 
#       (py36-tr) ➜ pip freeze > requirements.txt
#       (py36-tr) ➜ pip install -r requirements.txt
#
#  Utilizando:
#
#   import alerta_nt7 as tr  
#
# ------------------------------
__autor__ = "neviim jads - 2018"

from pymongo import MongoClient
from hashlib import md5, sha1
from lxml import html
from datetime import datetime
from pytz import timezone

import requests
import json

class AlertaNt7Terremotos(object):
    def __init__(self, url):
        super(AlertaNt7Terremotos, self).__init__()
        self.url = url
        self.div_xpath = '//div[@id="sismo_lista"]'
        self.div_dados = './/div[@style="padding-top:3px"]/text()'
        self.div_span  = './/span[@class="event-coordinates"]/text()'
        self.div_link  = './/a/@href'
        self.dados = []

    def cripto_md5(self, texto, encoding='utf-8'):
        """ Criptografa uma string retornando um valor de 32 bytes
        
            Arguments:
                texto {[str]}    -- [testo a ser criptografado]
            
            Keyword Arguments:
                encoding {str} -- [padrão ansi a ser utilizado no testo] (default: {'utf-8'})

            Retorno:
                texto criptografado.
        """
        return md5(texto.encode(encoding)).hexdigest()

    def cripto_sha1(self, texto, encoding='utf-8'):
        """ Criptografa uma string retornando um valor de 40 bytes
        
            Arguments:
                texto {[str]} -- [testo a ser criptografado]
            
            Keyword Arguments:
                encoding {str} -- [padão ansi a sr utilizado no testo] (default: {'utf-8'})

            Retorno:
                testo criptografado
        """
        return sha1(texto.encode(encoding)).hexdigest()

    def get_latitude(self, link):
        """ pega a latitude e a longitude do local do terremoto
        
            Arguments:
                link {[str]} -- [Contem o link de onde sera extraido a latitude e longitude]

            Retorno:
                {[list]} -- [contendo a latitude, longitude]
        """
        response = requests.get(link).text
        tree = html.fromstring(response)
        resultado = tree.xpath(self.div_span)

        # caso a lista esteja vazia, monta valor zerado para ser retornado.
        if len(resultado) == 0: 
            resultado = ['000.000°N  000.000°W']

        return resultado[0].split()

    def get_scraping(self):
        """ Estrai a lista com os ultimos 200 terremotos ocorridos.
        
            Retorno:
                self.dados [{lista}]    -- [lista com todos os 200 dados da lista de terremotos atualizados]
        """
        dados = []
        terremotos = []
        pagina = requests.get(self.url)

        print("Processando captura de dados...")

        # se pagina for encontrada.
        if pagina.status_code == 200:
            tree = html.fromstring(pagina.content)

            # as div_[xpath,dados,link] estao definidas em __init__
            for titles in tree.xpath(self.div_xpath):
                dados = titles.xpath(self.div_dados)
                links = titles.xpath(self.div_link )

                # pega a latitude/longitude desta ocorrencia.
                if len(links) > 0:
                    latitude = self.get_latitude(links[0])
                    dados.append(latitude)
                    terremotos.append(dados)

        return terremotos

    def formato_json(self, terremotos):
        """ doarquivo retornado da leitura de pagina dos 200 terremotos, monta um arquivo json
        
            Arguments:
                terremotos {[list]} -- [contem o retorno dos ultimos 200 terremotos registrados ate o momento]

            Retorno:
                dicionario no formato json com todos as 200 terromotos ocoridos.
        """
        registro = []

        print("Processando geração de json...")

        for terremoto in terremotos:
            # só se ouver registro sísmico a ser processado
            if len(terremoto) == 7:
                # somente se o terremoto tiver magnitude maior que 2.
                if ( float(terremoto[3]) >= 2 ):

                    # print( terremoto[6] )

                    # limpa e filtra dados a serem registrados.
                    data_hora_gmt  = terremoto[0].replace('\xa0','').split()
                    data_hora_bra  = terremoto[1].replace('\xa0','').split()
                    data_latitude  = terremoto[6][0]
                    data_longitude = terremoto[6][1]
                    data_key       = self.cripto_sha1(terremoto[0].replace('\xa0','')+terremoto[1].replace('\xa0','')+terremoto[3], encoding='utf-8')
                    # gera um registro de dados do terremoto
                    registro.append({
                        'data_gnt':        data_hora_gmt[0],
                        'hora_gnt':        data_hora_gmt[1],
                        'data_bra':        data_hora_bra[0],
                        'hora_bra':        data_hora_bra[1],
                        'intensidade':     float(terremoto[2]),
                        'magnitude':       float(terremoto[3]),
                        'profundidade':    terremoto[4].replace('\xa0','').split(),
                        'localidade_pais': terremoto[5].split(','),
                        'latitude':        float(data_latitude),
                        "longitude":       float(data_longitude),
                        'key':             data_key
                    })
        return registro

    def data_hora(self, localidade='America/Sao_Paulo', formato='%d/%m/%Y %H:%M'):
        """retorna data e hora local
        
            Keyword Arguments:
                localidade {str} -- [fuzorario a ser considerado para retornar a hora atual] (default: {'America/Sao_Paulo'})
                formato {str} -- [formato da hora e data a ser retornado, padrão brasil - sp] (default: {'%d/%m/%Y %H:%M'})
        """
        data_e_hora_atuais = datetime.now()
        fuso_horario = timezone(localidade)
        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
        data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime(formato)
        #
        return(data_e_hora_sao_paulo, data_e_hora_sao_paulo_em_texto)

    def grava_novas_ocorrencias(self, listjson, host='10.0.9.18', porta=27017):
        """ consulta uma nova lista dos 200 ultimos terremotos e grava no banco as ultimas ocorrencias
        
            Arguments:
                listjson {[list]} -- [lista contendo as ultimas 200 ocorrencias de terremoto no mundo]
            
            Keyword Arguments:
                host {str}  -- [host do banco de dados mongodb ao qual sera gravado estas novas ocorrencias] (default: {'devops.joaopauloii'})
                porta {int} -- [porta a qual o cliente mongodb deve se conectar] (default: {27017})
        """
        # conecta ao mongodb, defini collection terremoto
        client  = MongoClient(host, porta)
        db = client.terremotos
        collection = db['registros']

        print("Processando gravando em banco...")

        # grava cada (colection) registro no banco.
        for item in listjson:
            if collection.find_one({'key': item['key']}) == None: 
                rec_id = collection.insert_one(item)
                print(f"Registro: {item['key']} foi adicionado ao banco.")         

        # fecha conecção com o banco
        client.close()
        return

    def ultimos(self, quantidade=10):
        
        print( self.dados )

        #for item in range(1, quantidade+1):
        #    print(self.dados[item])
        return True


# -- main, 
def main():
    # utilizando class alertaNt7Terremotos estrair dados
    url = 'http://monitorglobal.com.br/terremotos.html'
    tjson = []

    # conecta no site e captura as 200 ultimas ocorrencias
    alertaTerremotos = AlertaNt7Terremotos(url)
    ultimos200 = alertaTerremotos.get_scraping()
    ultimos200_json = alertaTerremotos.formato_json(ultimos200)

    # os insidentes que nao estiver no banco serão gravados.
    alertaTerremotos.grava_novas_ocorrencias(ultimos200_json, "10.0.9.18")

    # retorna data e hora local em dois formatos
    #data1, data2 = alertaTerremotos.data_hora()
    #print(data1, data2)

    #alertaTerremotos.ultimos(10)
    # 

    # d = datetime.datetime(2009, 11, 12, 12)
    # for post in posts.find({"date": {"$lt": d}}).sort("author"):


# -- inicio
if __name__ == '__main__':
    main()



