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
#       $ conda activate \__CondaVirtual\pytr37
#       $ code .
#       $ conda deactivate
#
#       $ conda create --prefix \path_do_projeto\py37\ python=3.7
#       $ conda deactivate
#
#       $ cd \Users\jorge.FCN\Documents\GitHub\_python_projetos
#       $ cd /home/jorge/src/terremotos/src
#       $ source ~/virtual/py37/bin/activate
#
#       (py37-tr) ➜ 
#       (py37-tr) ➜ pip freeze > requirements.txt
#       (py37-tr) ➜ pip install -r requirements.txt
#
#  Utilizando:
#
#   import alerta_nt7 as tr  
#
# ------------------------------
__autor__ = "neviim jads - 2018"
__version__ = "0.2.0"

from pymongo import MongoClient
from hashlib import md5, sha1
from lxml import html
from datetime import datetime
from pytz import timezone
from geopy.geocoders import Nominatim

import requests
import config as cf
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
                encoding {str}   -- [padrão ansi a ser utilizado no testo] (default: {'utf-8'})

            Retorno:
                texto criptografado.
        """
        return md5(texto.encode(encoding)).hexdigest()

    def cripto_sha1(self, texto, encoding='utf-8'):
        """ Criptografa uma string retornando um valor de 40 bytes
        
            Arguments:
                texto {[str]}  -- [testo a ser criptografado]
            
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
                {[list]}     -- [contendo a latitude, longitude]
        """
        response = requests.get(link).text
        tree = html.fromstring(response)
        resultado = tree.xpath(self.div_span)

        # caso a lista esteja vazia, monta valor zerado para ser retornado.
        if len(resultado) == 0: 
            resultado = ['000.000°N  000.000°W']

        return resultado[0].split()

    def get_scraping(self):
        """ Extrai a lista com os ultimos 200 terremotos ocorridos.
        
            Retorno:
                self.dados [{lista}]  -- [lista com todos os 200 dados da lista de terremotos atualizados]
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
        """ do arquivo retornado da leitura de pagina dos 200 terremotos, monta um arquivo json
        
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
                    data_key = self.cripto_sha1(terremoto[0].replace('\xa0','')+terremoto[1].replace('\xa0','')+terremoto[3], encoding='utf-8')
                    
                    #não implementado.
                    #data_latitude, data_longitude = self.geo_localizacao(terremoto[5]) # pesquisa/processa e retorna latitude e longitude da localidade
                    
                    # gera um registro de dados do terremoto
                    registro.append({
                        'data_gnt':        data_hora_gmt[0],
                        'hora_gnt':        data_hora_gmt[1],
                        'data_bra':        data_hora_bra[0],
                        'hora_bra':        data_hora_bra[1],
                        'intensidade':     terremoto[2],
                        'magnitude':       terremoto[3],
                        'profundidade':    terremoto[4].replace('\xa0','').split(),
                        'localidade_pais': terremoto[5].split(','),
                        'latitude':        data_latitude,
                        "longitude":       data_longitude,
                        'key':             data_key
                    })
        return registro

    def data_hora(self, localidade=cf.localidade, formato='%d/%m/%Y %H:%M'):
        """ retorna data e hora local
        
            Keyword Arguments:
                localidade {str} -- [fuso horário a ser considerado para retornar a hora atual]  (default: {'America/Sao_Paulo'})
                formato {str}    -- [formato da hora e data a ser retornado, padrão brasil - sp] (default: {'%d/%m/%Y %H:%M'})
        """
        data_e_hora_atuais = datetime.now()
        fuso_horario = timezone(localidade)
        data_e_hora_sao_paulo = data_e_hora_atuais.astimezone(fuso_horario)
        data_e_hora_sao_paulo_em_texto = data_e_hora_sao_paulo.strftime(formato)
        #
        return(data_e_hora_sao_paulo, data_e_hora_sao_paulo_em_texto)

    def grava_novas_ocorrencias(self, listjson, host=cf.mongodb_host, porta=cf.mongodb_port):
        """ consulta uma nova lista dos 200 ultimos terremotos e grava no banco as ultimas ocorrencias
        
            Arguments:
                listjson {[list]} -- [lista contendo as ultimas 200 ocorrencias de terremoto no mundo]
            
            Keyword Arguments:
                host {str}  -- [host do banco de dados mongodb ao qual sera gravado estas novas ocorrencias] (default: {cf.mongodb_host})
                porta {int} -- [porta a qual o cliente mongodb deve se conectar] (default: {27017})
        """
        # conecta ao mongodb, defini collection terremoto
        client  = MongoClient(host, porta)
        db = client.terremotos
        collection = db['registros']

        print("Processando gravando em banco...\n")

        totalNovosTerremotos = 0

        # grava cada (colection) registro no banco.
        for item in listjson:
            if collection.find_one({'key': item['key']}) == None: 
                # grava a ocorrencia de terremoto em banco.
                rec_id = collection.insert_one(item)
                print(f"Registro: {item['key']} foi adicionado ao banco.")
                totalNovosTerremotos += 1

        # printa o total novos terremotos ocorrido de da ultima execução do script
        print()
        print("Total de novas ocorrencias: " +str(totalNovosTerremotos))
        print()

        # fecha conecção com o banco
        client.close()
        return

    def ultimos(self, quantidade=10):
        """ """
        print( self.dados )

        #for item in range(1, quantidade+1):
        #    print(self.dados[item])
        return True

    def geo_localizacao(self, localidade):
        """ Consulta site para pegar a latitude, longitude da localidade do terremoto
         
            Arguments:
                localidades {[vetor]} - [contem duas strings Localidade e pais] 

                Ex: ['10km WNW of Ndoi Island', ' Fiji']

            Variaveis:
                local[0] = Localidade
                local[1] = Pais
        """
        # local é um vetor["localidade", "pais"]
        conteudo = localidade.split(',')
        local = conteudo[0]
        pais = ""

        ### Refatorar esta abordagem ......................

        # algumas localidades estão sem o pais, < 1
        if len(conteudo) > 1: 
            pais = conteudo[1].strip()
        else: 
            # Esta opção trata casos como ilhas ex: (Fiji) 
            # pais por estar em branco recebera a região
            # Ex: 'South of the Fiji Islands', pais = "South" 
            sub_local = local.split(' of ')
            pais = sub_local[0]
          
        of_inicio = local.find(" of ") + 4   # encontra a posicao de "of" na string, (+4) seta ponteiro para proxima palavra.
        local = local[of_inicio:len(local)]  # remove a Km/SW deixando somente a localidade.

        # retorna a latitude e longitude da localidade
        geolocalizacao = Nominatim(user_agent="terremotos")
        locacao = geolocalizacao.geocode(local, pais)

        # caso nao tenha resultado com o local, procura só pelo pais
        if locacao == None:
            locacao = geolocalizacao.geocode(pais)
        
        print()
        print(conteudo)
        print(locacao)

        ### tratar localidade retornada maior que uma ...


        return (locacao.latitude, locacao.longitude)

# -- main, 
def main():
    # utilizando class alertaNt7Terremotos estrair dados
    url = cf.url_site_terremotos
    tjson = []

    # conecta no site e captura as 200 ultimas ocorrencias
    alertaTerremotos = AlertaNt7Terremotos(url)
    ultimos200 = alertaTerremotos.get_scraping()
    ultimos200_json = alertaTerremotos.formato_json(ultimos200)

    # os insidentes que nao estiver no banco serão gravados.
    alertaTerremotos.grava_novas_ocorrencias(ultimos200_json, cf.mongodb_host)

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



