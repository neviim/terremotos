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
        self.div_link  = '//a'
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

    def ultimos(self, quantidade=10):
        
        print( self.dados )

        #for item in range(1, quantidade+1):
        #    print(self.dados[item])
        return True

    def get_latitude(self, novo_link):
        """ pega a latitude e a longitude do local do terremoto
        
            Arguments:
                novo_link {[str]} -- [Contem o link de onde sera extraido a latitude e longitude]

            Retorno:
                {[list]} -- [contendo a latitude, longitude]
        """
        response = requests.get(novo_link).text
        tree = html.fromstring(response)
        resultado = tree.xpath('.//span[@class="event-coordinates"]/text()')
        
        # caso a lista esteja vazia, monta valor zerado para ser retornado.
        if len(resultado) == 0: 
            resultado = ['00.000°N', '000.000°W']

        return resultado[0].split()

    def scraping(self):
        """ Estrai a lista com os ultimos 200 terremotos ocorridos.
        
            Retorno:
                parametro1 [{borlean}] -- [campo logico True caso tudo corra bem e falso se der algo errado]
                parametro2 [{lista}]   -- [lista com todos os 200 dados da lista de ultimos terremotos]
        """
        dados  = []
        pagina = requests.get(self.url)

        # se pagina for encontrada.
        if pagina.status_code == 200:
            tree = html.fromstring(pagina.content)

            # uma xpath para extrair uma div
            div_main = tree.xpath('//div[@id="sismo_lista"]')

            # não ouvendo dados, retorna false.
            if div_main is None:
                return(False)

            # cria uma lista com os dados.
            for itens in div_main:
                dados.append(itens.xpath('.//div[@style="padding-top:3px"]/text()'))

        return(True, dados)

    def novo_scraping(self):
        """ Estrai a lista com os ultimos 200 terremotos ocorridos.
        
            Retorno:
                True [{borlean}]        -- [campo logico True caso tudo corra bem e falso se der algo errado]
                self.dados [{lista}]    -- [lista com todos os 200 dados da lista de terremotos atualizados]
        """
        jads = 0
        dados = []
        pagina = requests.get(self.url)

        # se pagina for encontrada.
        if pagina.status_code == 200:
            tree = html.fromstring(pagina.content)

            for titles in tree.xpath('//div[@id="sismo_lista"]'):
                dados = titles.xpath('.//div[@style="padding-top:3px"]/text()')
                links = titles.xpath(".//a/@href")

                #jads = jads + 1
                #print(links)
                
                #if jads == 10:
                #    break

                # pega a latitude/longitude desta ocorrencia.
                if len(links) > 0:
                    latitude = self.get_latitude(links[0])
                    dados.append(latitude)
                    #print(latitude)
                    #print(self.dados)
                    #print('--->', end='')

        return dados

    def cria_json(self, dados):
        """ doarquivo retornado da leitura de pagina dos 200 terremotos, monta um arquivo json
        
            Arguments:
                dados {[list]} -- [contem o retorno dos ultimos 200 terremotos registrados ate o momento]

            Retorno:
                dicionario no formato json com todos as 200 terromotos ocoridos.
        """
        registro = []

        # print( dados )

        for terremoto in dados[1]:
            
            # print( len(terremoto))

            if len(terremoto) == 6:

                #print(terremoto[3])
                #print(type(terremoto[3]))

                if ( float(terremoto[3]) >= 2 ):
                    data_hora_gmt  = terremoto[0].replace('\xa0','').split()
                    data_hora_bra  = terremoto[1].replace('\xa0','').split()
                    data_latitude  = terremoto[7][0]
                    data_longitude = terremoto[7][1]
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
                        'key': self.cripto_sha1(terremoto[0].replace('\xa0','')+terremoto[1].replace('\xa0','')+terremoto[3], encoding='utf-8')
                    })
        #jretorno = json.dumps(registro, sort_keys=True, indent=2)
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

    def grava_novas_ocorrencias(self, listjson, host='devops.joaopauloii', porta=27017):
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

        # grava cada (colection) registro no banco.
        for item in listjson:
            if collection.find_one({'key': item['key']}) == None: 
                rec_id = collection.insert_one(item)
                print(f"Registro: {item['key']} foi adicionado ao banco.")         

        # fecha conecção com o banco
        client.close()
        return

# -- main, 
def main():
    # utilizando class alertaNt7Terremotos estrair dados
    url = 'http://monitorglobal.com.br/terremotos.html'
    tjson = []

    # conecta no site e captura as 200 ultimas ocorrencias
    terremotos = AlertaNt7Terremotos(url)
    dadoslista = terremotos.novo_scraping()
    listjson   = terremotos.cria_json(dadoslista)

    #print(listjson)
    #return

    # os insidentes que nao estiver no banco serão gravados.
    terremotos.grava_novas_ocorrencias(listjson)

    # retorna data e hora local em dois formatos
    data1, data2 = terremotos.data_hora()
    print(data1, data2)

    ultimos10 = terremotos.ultimos(10)
    print(ultimos10)

    # d = datetime.datetime(2009, 11, 12, 12)
    # for post in posts.find({"date": {"$lt": d}}).sort("author"):


# -- inicio
if __name__ == '__main__':
    main()



