# TRATAMENTO DOS DADOS DO CNES, SIGTAP E TETO
## Autor: Otávio Augusto dos Santos
## Data: 2023-03-17

## Versão: 1.0
## Descrição: Tratamento dos dados do CNES, SIGTAP e TETO
## Entrada: Dados do CNES, SIGTAP e TETO
## Saída: Dados tratados do CNES, SIGTAP e TETO
## Observações:
## 1. O arquivo de entrada deve estar na pasta BASE 
## 2. O arquivo de saída será gerado no formato CSV
## 3. O arquivo de saída será salvo na pasta de BASE GERAL


# Importação das bibliotecas
import pandas as pd # Biblioteca para manipulação de dados
import os # Biblioteca para manipulação de arquivos
import re  # Biblioteca para expressões regulares
import time # Biblioteca para medir o tempo de execução
import warnings # Biblioteca para ignorar avisos
import zipfile # Biblioteca para manipulação de arquivos ZIP
warnings.filterwarnings("ignore")
tempo_inicial = time.time()
from glob import glob # Biblioteca para manipulação de arquivos
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

print(f'[OK] Início do processo:==========================> {time.time() - tempo_inicial:.2f} segundos')

#Criar pasta de saída e  arquivo txt resultado em modo de escrita
pasta_base = 'BASE GERAL'

try:
    os.makedirs(pasta_base, exist_ok=True) 
except OSError as erro:
    print(f'[ERRO] A pasta {pasta_base} já existe.{erro}')

arquivo = open(f'{pasta_base}/historico_resultado.txt', 'w')


# Estabelecimento CNES 2023
dado_cnes = glob('BASE/BASE_DE_DADOS_CNES*.ZIP')[0] 
colunas_c = ['CO_UNIDADE','CO_CNES','NO_RAZAO_SOCIAL','NO_FANTASIA','TP_UNIDADE','TP_GESTAO','CO_ESTADO_GESTOR','CO_MUNICIPIO_GESTOR','CO_MOTIVO_DESAB'] 

with zipfile.ZipFile(dado_cnes, 'r') as myzip:
    files = myzip.namelist() # Obtendo a lista de arquivos no ZIP
    df_cnes = next((file for file in files if re.match(r'tbEstabelecimento.*\.csv', file)), None) # Encontrando o arquivo CSV com a expressão regular
    
    if df_cnes:
        with myzip.open(df_cnes) as myfile:
            df_cnes = pd.read_csv(myfile, sep=';', encoding='latin-1', low_memory=False, usecols=colunas_c)
            df_cnes.columns.values # Exibindo os valores do arquivo 
            print(f"[OK] Importação do CNES:==========================> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)     
    else:
        print(f'[ERRO] Importação do CNES - Arquivo CSV não encontrado.', file=arquivo)
 

## Serviço x Classificação 2023
conlunas_s = ['CO_UNIDADE', 'CO_SERVICO', 'CO_CLASSIFICACAO']

with zipfile.ZipFile(dado_cnes, 'r') as myzip:
    files = myzip.namelist() # Obtendo a lista de arquivos no ZIP
    df_cnes_servicos = next((file for file in files if re.match(r'rlEstabServClass.*\.csv', file)), None) # Encontrando o arquivo CSV com a expressão regular
    
    if df_cnes_servicos:
        with myzip.open(df_cnes_servicos) as myfile:
            df_cnes_servicos = pd.read_csv(myfile, sep=';', encoding='latin-1', low_memory=False, usecols=conlunas_s)
            df_cnes_servicos.columns.values # Exibindo os valores do arquivo 
            print(f"[OK] Importação CNES - Serviço x Classificação:===> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)
    else:
        print(f'[ERRO] Importação CNES - Serviço x Classificação - Arquivo CSV não encontrado.', file=arquivo)


## Habilitação 2023
conlunas_h = ['CO_UNIDADE', 'COD_SUB_GRUPO_HABILITACAO']

with zipfile.ZipFile(dado_cnes, 'r') as myzip:
    files = myzip.namelist() # Obtendo a lista de arquivos no ZIP
    df_cnes_habilitacao = next((file for file in files if re.match(r'rlEstabSipac.*\.csv', file)), None) # Encontrando o arquivo CSV com a expressão regular
    
    if df_cnes_habilitacao:
        with myzip.open(df_cnes_habilitacao) as myfile:
            df_cnes_habilitacao = pd.read_csv(myfile, sep=';', encoding='latin-1', low_memory=False, usecols=conlunas_h)
            df_cnes_habilitacao.columns.values # Exibindo os valores do arquivo 
            print(f"[OK] Importação CNES - Habilitação:===============> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)
    else:
        print(f'[ERRO] Importação CNES - Habilitação - Arquivo CSV não encontrado.', file=arquivo)


### Habilitação e descrição 2023
colunas_h_d = ['CO_CODIGO_GRUPO', 'NO_DESCRICAO_GRUPO']

with zipfile.ZipFile(dado_cnes, 'r') as myzip:
    files = myzip.namelist() # Obtendo a lista de arquivos no ZIP
    df_cnes_habilitacao_desc = next((file for file in files if re.match(r'tbSubGruposHabilitacao.*\.csv', file)), None) # Encontrando o arquivo CSV com a expressão regular
    
    if df_cnes_habilitacao_desc:
        with myzip.open(df_cnes_habilitacao_desc) as myfile:
            df_cnes_habilitacao_desc = pd.read_csv(myfile, sep=';', encoding='latin-1', low_memory=False, usecols=colunas_h_d)
            df_cnes_habilitacao_desc.columns.values # Exibindo os valores do arquivo 
            print(f"[OK] Importação CNES - Habilitação e Descrição:===> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)
    else:
        print(f'[ERRO] Importação CNES - Habilitação e Descrição - Arquivo CSV não encontrado.', file=arquivo)

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
            print(f"[OK] Importação CNES - Leitos, leitos SUS:========> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)
    else:
        print(f'[ERRO] Importação CNES - Leitos, leitos SUS - Arquivo CSV não encontrado.', file=arquivo)


## Merge dos dados do CNES
df_base_cnes_s = pd.merge(df_cnes, df_cnes_servicos, on='CO_UNIDADE', how='left')
df_base_cnes_h = pd.merge(df_cnes, df_cnes_habilitacao, on='CO_UNIDADE', how='left')
df_base_cnes_l = pd.merge(df_cnes, df_cnes_leitos, on='CO_UNIDADE', how='left') 
print(f"[OK] Merge dos dados do CNES:=====================> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)


## Exportando os dados
dataframes = [df_base_cnes_s, df_base_cnes_h, df_base_cnes_l]

for i, df in enumerate(dataframes):
    nome_arquivo = f'{pasta_base}/.BASE_CNES_{i}.csv'
    df.to_csv(nome_arquivo, sep=';', encoding='latin-1', index=False)

print(f"[OK] Exportando os dados do CNES:=================> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)
## Fim do código


# Teto Mac 2023

dado_tetp = glob('BASE/*relatorioTetoFinanceiroBrasilExcel.xlsx')[0] 
df_teto_mac = pd.read_excel(dado_tetp, sheet_name='relatorioTetoFinanceiroBrasilEx')
df_teto_mac.drop(df_teto_mac.loc[df_teto_mac['Descrição Gestão']=='Total UF'].index, inplace=True)
print(f"[OK] Importação Teto Mac:=========================> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)

## Exportando os dados
df_teto_mac.to_csv(f'{pasta_base}\.BASE_TETO_MAC.csv', sep=';', encoding='latin-1', index=False)
## Fim do código


# SIGTAP 2023

dado_sigtap = glob('BASE/TabelaUnificada_2023*.zip')[0] 

with zipfile.ZipFile(dado_sigtap) as myzip: 
    with myzip.open('tb_procedimento.txt') as myfile:  
        df_sigtap = pd.read_fwf(myfile, colspecs=[(0,10), (10,260), (260,330)], 
                               names=["CO_PROCEDIMENTO", "NO_PROCEDIMENTO", "DT_COMPETENCIA"], encoding='latin')
df_sigtap.drop(['DT_COMPETENCIA'], axis=1, inplace=True)
print(f"[OK] Importação SIGTAP:===========================> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)


## SIGTAP - serviços / classificação 2023

with zipfile.ZipFile(dado_sigtap) as myzip: # Abrindo o arquivo zip
   with myzip.open('rl_procedimento_servico.txt') as myfile:  
      df_sigtap_servico = pd.read_fwf(myfile, colspecs=[(0,10), (10,13), (13,16), (16,22)], 
                              names=["CO_PROCEDIMENTO","CO_SERVICO","CO_CLASSIFICACAO","DT_COMPETENCIA"], encoding='latin') # Lendo o arquivo txt
df_sigtap_servico.drop(['DT_COMPETENCIA'], axis=1, inplace=True) # Removendo colunas desnecessárias
print(f"[OK] Importação SIGTAP - Serviços:================> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)


## SIGTAP -Habilitação 2023

with zipfile.ZipFile(dado_sigtap) as myzip: # Abrindo o arquivo zip
   with myzip.open('rl_procedimento_habilitacao.txt') as myfile:  
      df_sigtap_habilitacao = pd.read_fwf(myfile, colspecs=[(0,10), (10,14), (14,18), (18,24)], names=["CO_PROCEDIMENTO", "CO_HABILITACAO", "NU_GRUPO_HABILITACAO", "DT_COMPETENCIA"]) # Lendo o arquivo txt
df_sigtap_habilitacao.drop(['NU_GRUPO_HABILITACAO','DT_COMPETENCIA'], axis=1, inplace=True) # Removendo colunas desnecessárias
print(f"[OK] Importação SIGTAP - Habilitação:=============> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)


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
print(f"[OK] Importação SIGTAP - Forma de Registro:=======> {time.time() - tempo_inicial:.2f} segundos", file=arquivo)



















# Fechar arquivo txt
arquivo.close()
print(f"[OK] Fim do código:===============================> {time.time() - tempo_inicial:.2f} segundos")