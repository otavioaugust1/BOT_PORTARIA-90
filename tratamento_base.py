# TRATAMENTO DOS DADOS DO CNES, SIGTAP E TETO
## Autor: Otávio Augusto dos Santos
## Data: 2023-04-13

## Versão: 2.7.10
## Descrição: Tratamento dos dados do CNES, SIGTAP e TETO
## Entrada: Dados do CNES, SIGTAP e TETO
## Saída: Dados tratados do CNES, SIGTAP e TETO
## Observações:
## 1. O arquivo de entrada deve estar na pasta BASE 
## 2. O arquivo de saída será gerado no formato CSV
## 3. O arquivo de saída será salvo na pasta de BASE GERAL


# Importação das bibliotecas
import pandas as pd # importando a biblioteca pandas
import numpy as np # importando a biblioteca numpy
import time # importando a biblioteca time
import zipfile # importando a biblioteca zipfile
import shutil # Biblioteca para manipular arquivos e pastas
import urllib.request # Biblioteca para fazer download de arquivos
import openpyxl # Biblioteca para manipular arquivos excel
import re # importando a biblioteca re
import os # importando a biblioteca os
import ftplib # Biblioteca para fazer download de arquivos

#Warnings: Possui detalhes sobre os avisos e alertas que aparecem, porém podemos utiliza-lo também para que os alertas de
import warnings # não apareçam na tela
warnings.filterwarnings("ignore")  # Não exibe os avisos
tempo_inicial = time.time() # tempo inicial para calcular o tempo de execução do código

from datetime import date,  timedelta # Biblioteca para manipular datas
from glob import glob # Utilizado para listar arquivos de um diretório
from selenium import webdriver # Biblioteca para automatizar o navegador
from selenium.webdriver.common.by import By # Biblioteca para automatizar o navegador
from datetime import date # Biblioteca para manipular datas
from dateutil.relativedelta import relativedelta # Biblioteca para manipular datas

pd.set_option('display.max_columns', None) # Comando para exibir todas colunas do arquivo
pd.set_option('display.max_rows', None) # Comando para exibir todas linhas do arquivo

start_time = time.time() # tempo inicial para calcular o tempo de execução do código

print(f"[OK] Início do processo:=====================================================>: {time.strftime('%H:%M:%S')}")

# formatação de datas para o nome dos arquivos
data_atual = date.today() # Data atual
data_corrente = date.today().strftime('%Y%m') # Data atual no formato YYYYMM
data_passada = (date.today() - relativedelta(months=1)).strftime('%Y%m') # Data atual menos 1 mês no formato YYYYMM
data_passada_a = (date.today() - relativedelta(months=2)).strftime('%Y%m') # Data atual menos 2 mês no formato YYYYMM


#Criar pasta de entrada, saida e  arquivo txt resultado em modo de escrita
pasta_entrada = 'BASE/' # Pasta onde estão os arquivos de entrada
pasta_saida = 'RESULTADOS/' # Pasta onde serão gravados os arquivos de saída
pasta_planilha = 'PLANILHA/' # Pasta onde serão gravados os arquivos para ser analisados (planilha)

for pasta in [pasta_entrada, pasta_saida, pasta_planilha]:
    try:
        os.mkdir(pasta)
    except OSError:
        pass

    for arquivo in os.listdir(pasta):
        arquivo_pasta = os.path.join(pasta, arquivo)
        try:
            if os.path.isfile(arquivo_pasta) or os.path.islink(arquivo_pasta):
                os.unlink(arquivo_pasta) # deleta o arquivo
            elif os.path.isdir(arquivo_pasta):
                shutil.rmtree(arquivo_pasta) # deleta o diretório
        except Exception as e:
            print(f'Falha ao deletar {arquivo_pasta}. Motivo: {e}')
print(f"[OK] Criando as pastas ======================================================>: {time.strftime('%H:%M:%S')}")


# Download dos arquivos CNES
url_c = f'ftp://ftp.datasus.gov.br/cnes/BASE_DE_DADOS_CNES_{data_passada}.ZIP'
filename_c = pasta_entrada + f'BASE_DE_DADOS_CNES_{data_passada}.ZIP'

try:
    with urllib.request.urlopen(url_c) as response, open(filename_c, 'wb') as out_file:
        data = response.read()  # Lê os dados do arquivo
        out_file.write(data)  # Escreve os dados em um arquivo local
except urllib.error.URLError:
    url_c = f'ftp://ftp.datasus.gov.br/cnes/BASE_DE_DADOS_CNES_{data_passada_a}.ZIP'
    filename_c = pasta_entrada + f'BASE_DE_DADOS_CNES_{data_passada_a}.ZIP'
    with urllib.request.urlopen(url_c) as response, open(filename_c, 'wb') as out_file:
        data = response.read()  # Lê os dados do arquivo
        out_file.write(data)  # Escreve os dados em um arquivo local

print(f"[OK] Download dos arquivos CNES =============================================>: {time.strftime('%H:%M:%S')}")


# Download dos arquivos SIGTAP
ftp = ftplib.FTP('ftp2.datasus.gov.br') # Conecta ao servidor FTP
ftp.login() # Faz login no servidor FTP
ftp.cwd('/pub/sistemas/tup/downloads/') # Navega até o diretório desejado

arquivos = ftp.nlst() # Lista os arquivos disponíveis
arquivo = [a for a in arquivos if a.startswith(f'TabelaUnificada_{data_corrente}') and a.endswith('.zip')]
arquivo_a = [a for a in arquivos if a.startswith(f'TabelaUnificada_{data_passada}') and a.endswith('.zip')]

if arquivo:
    url_s = f'ftp://ftp2.datasus.gov.br/pub/sistemas/tup/downloads/{arquivo[0]}'
    filename_s = pasta_entrada + f'BASE_DE_DADOS_SIGTAP_{data_corrente}.ZIP'

    with urllib.request.urlopen(url_s) as response, open(filename_s, 'wb') as out_file:
        data = response.read()  # Lê os dados do arquivo
        out_file.write(data)  # Escreve os dados em um arquivo local

    print(f"[OK] Download dos arquivos SIGTAP ===========================================>: {time.strftime('%H:%M:%S')}")
else:
    url_s = f'ftp://ftp2.datasus.gov.br/pub/sistemas/tup/downloads/{arquivo_a[0]}'
    filename_s = pasta_entrada + f'BASE_DE_DADOS_SIGTAP_{data_passada}.ZIP'

    with urllib.request.urlopen(url_s) as response, open(filename_s, 'wb') as out_file:
        data = response.read()  # Lê os dados do arquivo
        out_file.write(data)  # Escreve os dados em um arquivo local
    print(f"[OK] Download dos arquivos SIGTAP - MES ANTERIOR ============================>: {time.strftime('%H:%M:%S')}")


# Download dos arquivos SAIPS
''' 
url = 'https://www.gov.br/saude/pt-br/composicao/saes/saips/plano-atendimento-perf-cir-eletiva-vrs-4a.xlsx'
filename = pasta_entrada + f'BASE_DE_DADOS_SAIPS_V4.xlsx'

with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
    data = response.read()  # Lê os dados do arquivo
    out_file.write(data)  # Escreve os dados em um arquivo local
'''
print(f"[OK] Download do arquivo BASE_DE_DADOS_SAIPS.xlsx ===========================>: {time.strftime('%H:%M:%S')}")


# Download dos arquivos TETO FINANCEIRO BRASIL
url_t = 'https://sismac.saude.gov.br/teto_financeiro_brasil#'
filename = pasta_entrada + f'BASE_DE_DADOS_TETO_FINANCEIRO_BRASIL.xlsx'


#options = webdriver.EdgeOptions()
#options.use_chromium = True
#options.add_argument('--headless')
#options.add_argument('--disable-gpu')
#options.add_argument('--no-sandbox')
#options.add_argument('--disable-dev-shm-usage')

#driver = webdriver.Edge(executable_path=r'NAVEGADOR\msedgedriver.exe', options=options)
#driver.get(url_t)

#element = driver.find_element(By.XPATH, '//*[@id="conteudoPanel"]/div[3]/div/div/div[2]/p/a')
#element.click()

#driver.quit()

print(f"[OK] Download do arquivo BASE_DE_DADOS_TETO_MAC.xlsx ========================>: {time.strftime('%H:%M:%S')}")


#=============TRATAMENTO DOS DADOS==================

# Estabelecimento CNES 2023
dado_cnes = glob('BASE/BASE_DE_DADOS_CNES*.ZIP')[0] # Listando os arquivos do diretório
colunas_c = ['CO_UNIDADE','CO_CNES','NO_RAZAO_SOCIAL','NO_FANTASIA','TP_UNIDADE','TP_GESTAO','CO_ESTADO_GESTOR','CO_MUNICIPIO_GESTOR','CO_MOTIVO_DESAB'] 

with zipfile.ZipFile(dado_cnes, 'r') as myzip:
    files = myzip.namelist() # Obtendo a lista de arquivos no ZIP
    df_cnes = next((file for file in files if re.match(r'tbEstabelecimento.*\.csv', file)), None) # Encontrando o arquivo CSV com a expressão regular
    
    if df_cnes:
        with myzip.open(df_cnes) as myfile:
            df_cnes = pd.read_csv(myfile, sep=';', encoding='latin-1', low_memory=False, usecols=colunas_c)
            df_cnes.columns.values # Exibindo os valores do arquivo 
            print(f"[OK] Importação do CNES:=====================================================>: {time.strftime('%H:%M:%S')}")     
    else:
            print(f"[ERRO] Importação do CNES - Arquivo CSV não encontrado ======================>: {time.strftime('%H:%M:%S')}")
 

## Serviço x Classificação 2023
conlunas_s = ['CO_UNIDADE', 'CO_SERVICO', 'CO_CLASSIFICACAO']

with zipfile.ZipFile(dado_cnes, 'r') as myzip:
    files = myzip.namelist() # Obtendo a lista de arquivos no ZIP
    df_cnes_servicos = next((file for file in files if re.match(r'rlEstabServClass.*\.csv', file)), None) # Encontrando o arquivo CSV com a expressão regular
    
    if df_cnes_servicos:
        with myzip.open(df_cnes_servicos) as myfile:
            df_cnes_servicos = pd.read_csv(myfile, sep=';', encoding='latin-1', low_memory=False, usecols=conlunas_s)
            df_cnes_servicos.columns.values # Exibindo os valores do arquivo 
            print(f"[OK] Importação CNES - Serviço x Classificação ==============================>: {time.strftime('%H:%M:%S')}")
    else:
            print(f"[ERRO] Importação CNES - Serviço x Classificação [Arquivo não encontrado] ===>: {time.strftime('%H:%M:%S')}")


## Habilitação 2023
conlunas_h = ['CO_UNIDADE', 'COD_SUB_GRUPO_HABILITACAO']

with zipfile.ZipFile(dado_cnes, 'r') as myzip:
    files = myzip.namelist() # Obtendo a lista de arquivos no ZIP
    df_cnes_habilitacao = next((file for file in files if re.match(r'rlEstabSipac.*\.csv', file)), None) # Encontrando o arquivo CSV com a expressão regular
    
    if df_cnes_habilitacao:
        with myzip.open(df_cnes_habilitacao) as myfile:
            df_cnes_habilitacao = pd.read_csv(myfile, sep=';', encoding='latin-1', low_memory=False, usecols=conlunas_h)
            df_cnes_habilitacao.columns.values # Exibindo os valores do arquivo 
            print(f"[OK] Importação CNES - Habilitação ==========================================>: {time.strftime('%H:%M:%S')}")
    else:
            print(f'[ERRO] Importação CNES - Habilitação - [Arquivo CSV não encontrado] =========>: {time.strftime("%H:%M:%S")}')


### Habilitação e descrição 2023
colunas_h_d = ['CO_CODIGO_GRUPO', 'NO_DESCRICAO_GRUPO']

with zipfile.ZipFile(dado_cnes, 'r') as myzip:
    files = myzip.namelist() # Obtendo a lista de arquivos no ZIP
    df_cnes_habilitacao_desc = next((file for file in files if re.match(r'tbSubGruposHabilitacao.*\.csv', file)), None) # Encontrando o arquivo CSV com a expressão regular
    
    if df_cnes_habilitacao_desc:
        with myzip.open(df_cnes_habilitacao_desc) as myfile:
            df_cnes_habilitacao_desc = pd.read_csv(myfile, sep=';', encoding='latin-1', low_memory=False, usecols=colunas_h_d)
            df_cnes_habilitacao_desc.columns.values # Exibindo os valores do arquivo 
            print(f"[OK] Importação CNES - Habilitação e Descrição ==============================>: {time.strftime('%H:%M:%S')}")
    else:
            print(f'[ERRO] Importação CNES - Habilitação e Descrição - [Arquivo não encontrado] =>: {time.strftime("%H:%M:%S")}')

df_cnes_habilitacao = pd.merge(df_cnes_habilitacao, df_cnes_habilitacao_desc, left_on='COD_SUB_GRUPO_HABILITACAO', right_on='CO_CODIGO_GRUPO', how='left')
df_cnes_habilitacao.drop(['COD_SUB_GRUPO_HABILITACAO'], axis=1, inplace=True)


## Leitos / Leitos UTI 2023
colunas_l = ['CO_UNIDADE', 'CO_LEITO', 'CO_TIPO_LEITO','QT_EXIST','QT_SUS']

with zipfile.ZipFile(dado_cnes, 'r') as myzip:
    files = myzip.namelist() # Obtendo a lista de arquivos no ZIP
    df_cnes_leitos = next((file for file in files if re.match(r'rlEstabComplementar.*\.csv', file)), None) # Encontrando o arquivo CSV com a expressão regular
    
    if df_cnes_leitos:
        with myzip.open(df_cnes_leitos) as myfile:
            df_cnes_leitos = pd.read_csv(myfile, sep=';', encoding='latin-1', low_memory=False, usecols=colunas_l)
            df_cnes_leitos.columns.values # Exibindo os valores do arquivo 
            print(f"[OK] Importação CNES - Leitos, leitos SUS ===================================>: {time.strftime('%H:%M:%S')}")
    else:
            print(f'[ERRO] Importação CNES - Leitos, leitos SUS - [Arquivo não encontrado] ======>: {time.strftime("%H:%M:%S")}')


## Merge dos dados do CNES
df_base_cnes_s = pd.merge(df_cnes, df_cnes_servicos, on='CO_UNIDADE', how='left')
df_base_cnes_h = pd.merge(df_cnes, df_cnes_habilitacao, on='CO_UNIDADE', how='left')
df_base_cnes_l = pd.merge(df_cnes, df_cnes_leitos, on='CO_UNIDADE', how='left') 
print(f"[OK] Merge dos dados do CNES ================================================>: {time.strftime('%H:%M:%S')}")


## Exportando os dados
df_base_cnes_s.to_csv('BASE\.BASE_CNES_SERVICOS.csv', sep=';', encoding='latin-1', index=False) # Exportando o arquivo para csv
df_base_cnes_h.to_csv('BASE\.BASE_CNES_HABILITACAO.csv', sep=';', encoding='latin-1', index=False) # Exportando o arquivo para csv
df_base_cnes_l.to_csv('BASE\.BASE_CNES_LEITOS.csv', sep=';', encoding='latin-1', index=False) # Exportando o arquivo para csv

print(f"[OK] Exportando os dados do CNES ============================================>: {time.strftime('%H:%M:%S')}")
## Fim do código


# Teto Mac 2023

dado_tetp = glob('BASE-T/*relatorioTetoFinanceiroBrasilExcel.xlsx')[0] 
df_teto_mac = pd.read_excel(dado_tetp, sheet_name='relatorioTetoFinanceiroBrasilEx')
df_teto_mac.drop(df_teto_mac.loc[df_teto_mac['Descrição Gestão']=='Total UF'].index, inplace=True)
print(f"[OK] Importação Teto MAC  ===================================================>: {time.strftime('%H:%M:%S')}")

## Exportando os dados
df_teto_mac.to_csv(f'{pasta_entrada}\.BASE_TETO_MAC.csv', sep=';', encoding='latin-1', index=False)
## Fim do código


# SIGTAP 2023

dado_sigtap = glob('BASE/BASE_DE_DADOS_SIGTAP_2023*.zip')[0] 

with zipfile.ZipFile(dado_sigtap) as myzip: 
    with myzip.open('tb_procedimento.txt') as myfile:  
        df_sigtap = pd.read_fwf(myfile, colspecs=[(0,10), (10,260), (260,330)], 
                               names=["CO_PROCEDIMENTO", "NO_PROCEDIMENTO", "DT_COMPETENCIA"], encoding='latin')
df_sigtap.drop(['DT_COMPETENCIA'], axis=1, inplace=True)
print(f"[OK] Importação SIGTAP ======================================================>: {time.strftime('%H:%M:%S')}")


## SIGTAP - serviços / classificação 2023

with zipfile.ZipFile(dado_sigtap) as myzip: # Abrindo o arquivo zip
   with myzip.open('rl_procedimento_servico.txt') as myfile:  
      df_sigtap_servico = pd.read_fwf(myfile, colspecs=[(0,10), (10,13), (13,16), (16,22)], 
                              names=["CO_PROCEDIMENTO","CO_SERVICO","CO_CLASSIFICACAO","DT_COMPETENCIA"], encoding='latin') # Lendo o arquivo txt
df_sigtap_servico.drop(['DT_COMPETENCIA'], axis=1, inplace=True) # Removendo colunas desnecessárias
print(f"[OK] Importação SIGTAP - Serviços ===========================================>: {time.strftime('%H:%M:%S')}")


## SIGTAP -Habilitação 2023

with zipfile.ZipFile(dado_sigtap) as myzip: # Abrindo o arquivo zip
   with myzip.open('rl_procedimento_habilitacao.txt') as myfile:  
      df_sigtap_habilitacao = pd.read_fwf(myfile, colspecs=[(0,10), (10,14), (14,18), (18,24)], names=["CO_PROCEDIMENTO", "CO_HABILITACAO", "NU_GRUPO_HABILITACAO", "DT_COMPETENCIA"]) # Lendo o arquivo txt
df_sigtap_habilitacao.drop(['NU_GRUPO_HABILITACAO','DT_COMPETENCIA'], axis=1, inplace=True) # Removendo colunas desnecessárias
print(f"[OK] Importação SIGTAP - Habilitação ========================================>: {time.strftime('%H:%M:%S')}")


## SIGTAP - Forma de registro 2023

with zipfile.ZipFile(dado_sigtap) as myzip: # Abrindo o arquivo zip
   with myzip.open('rl_procedimento_registro.txt') as myfile:  
      df_sigtap_modalidade = pd.read_fwf(myfile, colspecs=[(0,10), (10,12), (12,18)], names=["CO_PROCEDIMENTO", "CO_REGISTRO", "DT_COMPETENCIA"]) # Lendo o arquivo txt
df_sigtap_modalidade.drop(['DT_COMPETENCIA'], axis=1, inplace=True) # Removendo colunas desnecessárias

with zipfile.ZipFile(dado_sigtap) as myzip: # Abrindo o arquivo zip
   with myzip.open('tb_registro.txt') as myfile:  
      df_sigtap_registro = pd.read_fwf(myfile, colspecs=[(0,2), (2,52), (52,58)], names=["CO_REGISTRO", "NO_REGISTRO", "DT_COMPETENCIA"], encoding='latin') # Lendo o arquivo txt
df_sigtap_registro.drop(['DT_COMPETENCIA'], axis=1, inplace=True) # Removendo colunas desnecessárias
df_sigtap_modalidade = pd.merge(df_sigtap_modalidade, df_sigtap_registro, on='CO_REGISTRO', how='left') # Juntando os arquivos
print(f"[OK] Importação SIGTAP - Forma de Registro ==================================>: {time.strftime('%H:%M:%S')}")


## SIGTAP - PLANILHA
df_planilha_proc = glob('BASE-T\BASE_DE_DADOS_SAIPS*.xlsx')[0] # Listando os arquivos do diretório
df_planilha_proc = pd.read_excel(df_planilha_proc, sheet_name='PROCEDIMENTOS') # Lendo o arquivo excel
df_planilha_proc.rename(columns={'Código do Procedimento':'CO_PROCEDIMENTO','Unnamed: 1':'SUBGRUPO','Unnamed: 2':'COD_PROCEDIMENTO', 'Unnamed: 3':'DEC_PROCEDIMENTO', 'Unnamed: 4':'codigo', 
                                 'Dados de Produção Brasil (2018 a 2022)':'QT_PROD_SIASUS', 'Unnamed: 6':'% ELET SIASUS', 'Unnamed: 7':'QT_PROD AIH 2018 a 2022',
                                 'Unnamed: 8':'% ELET AIH', 'Exigência SIGTAP':'EXIGE SERVIÇO', 'Unnamed: 10':'EXIGE HABILITACAO', 'Instrumento de REGISTRO':'BPA_I',
                                 'Unnamed: 12':'AIH', 'Unnamed: 13':'APAC'}, inplace=True) # Renomeando colunas
df_planilha_proc.drop(0, inplace=True) # Remove a primeira linha do arquivo
df_planilha_proc.drop(['codigo'], axis=1, inplace=True) # Remove a coluna codigo


## Juntando os arquivos - SIGTAP
df_sigtap_f = pd.merge(df_planilha_proc, df_sigtap_modalidade, left_on='COD_PROCEDIMENTO', right_on='CO_PROCEDIMENTO', how='left') # Juntando os arquivos 3
df_sigtap_f = pd.merge(df_sigtap_f, df_sigtap_servico, on='CO_PROCEDIMENTO', how='left') # Juntando os arquivos
df_sigtap_f = pd.merge(df_sigtap_f, df_sigtap_habilitacao, on='CO_PROCEDIMENTO', how='left') # Juntando os arquivos
df_sigtap_f.drop(['CO_PROCEDIMENTO'], axis=1, inplace=True) # Removendo colunas desnecessárias
print(f"[OK] Juntando os arquivos - SIGTAP:==========================================>: {time.strftime('%H:%M:%S')}")

## Exportando o arquivo
df_sigtap_f.to_csv('BASE\.BASE_SIGTAP_GERAL.csv', sep=';', encoding='latin-1', index=False) # Exportando o arquivo para csv
print(f"[OK] Exportando o arquivo - SIGTAP ==========================================>: {time.strftime('%H:%M:%S')}")

## Fechando os arquivos
myfile.close()
print(f"[OK] Fim do código  =========================================================>: {time.strftime('%H:%M:%S')}")