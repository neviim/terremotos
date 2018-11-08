# -*- coding: UTF-8 -*-
#
# ArangoDB v3.0
#
from hashlib import md5, sha1
from lxml import html
from datetime import datetime
from pytz import timezone
from pyArango.connection import *

import requests
import json


class CapturaTerremotos(object):
    def __init__(self):
        super(CapturaTerremotos, self).__init__()
        self.url = 'http://monitorglobal.com.br/terremotos.html'
        self.div_xpath = '//div[@id="sismo_lista"]'
        self.div_dados = './/div[@style="padding-top:3px"]/text()'
        self.div_span  = './/span[@class="event-coordinates"]/text()'
        self.div_link  = './/a/@href'
        self.dados = []

    def criptoMD5(self, texto, encoding='utf-8'):
        """ Criptografa uma string retornando um valor de 32 bytes
        
            Arguments:
                texto {[str]}    -- [testo a ser criptografado]
            
            Keyword Arguments:
                encoding {str} -- [padrão ansi a ser utilizado no testo] (default: {'utf-8'})

            Retorno:
                texto criptografado.
        """
        return md5(texto.encode(encoding)).hexdigest()

    def gravaEmArangoDB(self, terremotos):

        conn = Connection( arangoURL="http://10.0.9.18:8529", username="terremoto", password="terremoto" )

        # Abre ou cria Database
        if conn.hasDatabase("terremotosdb"):
            db = conn["terremotosdb"]
        else:
            db = conn.createDatabase(name="terremotosdb")

        # Abre ou cria Collection
        if db.hasCollection("terremotos"):
            terremotosCollection = db["terremotos"]
        else: 
            terremotosCollection = db.createCollection(name="terremotos")

        print("Gravando itens no banco (arangodb).")

        for item in terremotos:
            # Cria estrutura de dados para banco terremotosdb collection terremotos

            #print(terremotos)
            #print(len(terremotos))

            # terremotos um item:
            # [['08/11/2018', '15:01'], ['08/11/2018', '12:01'], 'Terremoto Moderado', 4.6, 
            #  [19.98, 'km'], [[41.0, 'km', 'ESE'], 'of Kulob', ' Tajikistan']]
            if len(terremotos) == 6:


                # parado aqui com erro:
                #               File "arangomot.py", line 77, in gravaEmArangoDB
                #               doc['intensidade' ] = item[2]
                #               IndexError: list index out of range


                print(terremotos)
                print(item)

                doc = terremotosCollection.createDocument()
                doc._key = ''.join(["jadsid:", self.criptoMD5(str(item))]).lower()
                doc['dataGmt'     ] = item[0][0]
                doc['horaGmt'     ] = item[0][1]
                doc['dataBra'     ] = item[1][0]
                doc['horaBra'     ] = item[1][1]
                doc['intensidade' ] = item[2]
                doc['magnitude'   ] = item[3]
                doc['profundidade'] = item[4]
                doc['localidade'  ] = item[5]
                doc.save()

        return

    def trataLocalidade(self, local):
        # pega primeiro caracter, verifica se é numerico.
        # regiao = ['116km N of Visokoi Island', ' South Georgia and the South Sandwich Islands']
        primeiroCaracter = local[0][0]
        localidadeTratada = local

        # caso o primeiro caracter seja numerico.
        if primeiroCaracter.isnumeric():
            # estrai a kilometragem e a direção
            distancia = local[0].split()[0][:-2]  # String 116km remove os 2 ultimos caracter km [:-2], retornando 116.
            unidadeMedida = local[0].split()[0][-2:]  # String 116km captura os 2 ultimos caracter [-2:], km.
            pontoCardial = local[0].split()[1]  # Estrai a segunda opção da lista em [local], ponto cardial (N)

            # monta uma nova lista com os resultados, estraidos e tratados.
            localidade = [float(distancia), unidadeMedida, pontoCardial]
            fazerCorte = len(str(localidade[0])) + len(localidade[1]) + len(localidade[2])
            localidadeTratada = [localidade, local[0][fazerCorte:], local[1]]
            
            #print(localidade)
            #print(fazerCorte)
            #print(localidadeTratada)
            
        return localidadeTratada

    def getLatitude(self, link):
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

        # separa e converte para numerico float
        lat, lon = resultado[0].split()
        resultado = [float(lat[:-2]), float(lon[:-2])]

        return resultado

    def getScraping(self):
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

            conta = 0  # Temporario

            # as div_[xpath,dados,link] estao definidas em __init__
            for titles in tree.xpath(self.div_xpath):
                dados = titles.xpath(self.div_dados)
                links = titles.xpath(self.div_link )

                # pega a latitude/longitude desta ocorrencia.
                if len(links) > 0:
                    #latitude = self.getLatitude(links[0])
                    #dados.append(latitude)

                    # trata os dados captirado, para armazena-lo em banco.
                    dataHoraGmt  = dados[0].replace('\xa0','').split()
                    dataHoraBra  = dados[1].replace('\xa0','').split()
                    profundidade = dados[4].replace('\xa0','').split()
                    localidade   = dados[5]

                    # Data/Hora GMT
                    #dataHoraGmt[0] = datetime.strptime(dataHoraGmt[0], "%d/%m/%Y").date()
                    #dataHoraGmt[1] = datetime.strptime(dataHoraGmt[1], '%H:%M').time()

                    # Data/Hora Brasilia
                    #dataHoraBra[0] = datetime.strptime(dataHoraBra[0], "%d/%m/%Y").date()
                    #dataHoraBra[1] = datetime.strptime(dataHoraBra[1], '%H:%M').time()

                    # Remonta a lista com os dados tratados
                    dados[0] = [dataHoraGmt[0], dataHoraGmt[1]]
                    dados[1] = [dataHoraBra[0], dataHoraBra[1]]
                    dados[3] = float(dados[3])
                    dados[4] = [float(profundidade[0]), profundidade[1]]

                    # tratando localidade
                    dados[5] = self.trataLocalidade(localidade.split(','))

                    # grava dados em banco.
                    terremotos.append(dados)
                    self.gravaEmArangoDB(dados)

                    #print(dados)

                # Rotina Temporaria -------
                conta = conta + 1
                if conta == 5: 
                    #print(terremotos)
                    return
                # Fim rotina temporaria ---

        return terremotos

def main():
    # utilizando class alertaNt7Terremotos estrair dados
    capturaTerremotos = CapturaTerremotos()
    ultimos200Terremotos = capturaTerremotos.getScraping()

    #print(ultimos200Terremotos)
    #put_arango() 

if __name__ == '__main__':
    main()