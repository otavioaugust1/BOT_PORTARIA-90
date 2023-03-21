# VALIDAÇÃO DAS PLANILHAS DE DADOS - PLANOS DE SAÚDE
## Autor: Otávio Augusto dos Santos
## Data: 2023-03-21

## Versão: 1.0
## Descrição: Validação dos dados de planos de saúde
## Entrada: Planilha do plano de saúde - SAIPS  
## Saída: arquivo TXT com os erros encontrados e arquivo xlsx com os dados corrigidos
## Observações:
## 1. O arquivo de entrada deve estar na pasta PLANILHA 
## 2. O arquivo de saída será gerado no formato TXT e XLSX
## 3. O arquivo de saída será salvo na pasta de RESULTADOS

# Importação das bibliotecas
import pandas as pd #biblioteca para manipulação de dados
import numpy as np #biblioteca para manipulação de dados
import os #biblioteca para manipulação de arquivos
import re #biblioteca para manipulação de expressões regulares
import time #biblioteca para manipulação de tempo
import xlsxwriter #biblioteca para manipulação de arquivos xlsx
import warnings #biblioteca para manipulação de avisos
from glob import glob #biblioteca para manipulação de arquivos
warnings.filterwarnings('ignore') #ignorar avisos
tempo_inicial = time.time() #tempo de início do processo

pd.set_option('display.max_columns', None) #mostrar todas as colunas
pd.set_option('display.max_rows', None) #mostrar todas as linhas

print(f'[OK] Início do processo:==========================> {time.time() - tempo_inicial:.2f} segundos')

#Criar pasta de saída e  arquivo txt resultado em modo de escrita
pasta_base = 'RESULTADOS'

try:
    os.makedirs(pasta_base, exist_ok=True) 
except OSError as erro:
    print(f'[ERRO] A pasta {pasta_base} já existe.{erro}')

arquivo = open(f'{pasta_base}/historico_resultado.txt', 'w')
print(f"============================== INFORMAÇÕES DO CARREGAMENTO ======================= \n \n", file=arquivo)

# base de dados
df_cnes_leitos = pd.read_csv('BASE\.BASE_CNES_LEITOS.csv', sep=';', encoding='latin-1', dtype=str)
df_cnes_habilitacao = pd.read_csv('BASE\.BASE_CNES_HABILITACAO.csv', sep=';', encoding='latin-1', dtype=str)
df_cnes_servicos = pd.read_csv('BASE\.BASE_CNES_SERVICOS.csv', sep=';', encoding='latin-1', dtype=str)
print(f'[OK] Base de CNES carregada:======================> {time.time() - tempo_inicial:.2f} segundos' ,file=arquivo)

df_sigtap = pd.read_csv('BASE\.BASE_SIGTAP_GERAL.csv', sep=';', encoding='latin-1', dtype=str)
df_sigtap['COD_PROCEDIMENTO']= df_sigtap['COD_PROCEDIMENTO'].astype(int) # Converte a coluna 'COD_PROCEDIMENTO' para string
df_sigtap['QT_PROD AIH 2018 a 2022']= df_sigtap['QT_PROD AIH 2018 a 2022'].astype(int) # Converte a coluna 'QT_PROD AIH 2018 a 2022' para string
df_sigtap.head() # Exibe as 5 primeiras linhas do arquivo
print(f'[OK] Base de SIGTAP carregada:====================> {time.time() - tempo_inicial:.2f} segundos',file=arquivo)

df_teto = pd.read_csv('BASE\.BASE_TETO_MAC.csv', sep=';', encoding='latin-1', dtype=str)
print(f'[OK] Base de TETO MAC carregada:==================> {time.time() - tempo_inicial:.2f} segundos',file=arquivo)


# Planilha para ser validada
## ABA 1

df_planilha = glob('PLANILHA\*.xlsx')[0] # Planilha para ser validada
df_planilha_aba1 = pd.read_excel(df_planilha, sheet_name='Ident. Fila na UF') # Lê o arquivo excel
df_planilha_aba1.rename(columns={'PLANO ESTADUAL DE REDUÇÃO DE FILAS DE ESPERA EM CIRURGIAS ELETIVAS - FILA DE ESPERA':'COD_PROCEDIMENTO','Unnamed: 1':'DESC_PROCEDIMENTO','Unnamed: 2':'QUANT_FILA', 
                                 'Unnamed: 3':'PERC_REDUCAO', 'Unnamed: 4':'TEMPO_MESES', 'Unnamed: 5':'QUANT_REDUCAO', 'Unnamed: 6':'LINHA'}, inplace=True) 
                                # Renomeia a coluna 'PLANO ESTADUAL DE REDUÇÃO DE FILAS DE ESPERA EM CIRURGIAS ELETIVAS - FILA DE ESPERA' para 'UF'
df_planilha_aba1.drop(0, inplace=True) # Remove a primeira linha do arquivo
df_planilha_aba1.drop(1, inplace=True) # Remove a segunda linha do arquivo
df_planilha_aba1.drop(df_planilha_aba1.tail(1).index,inplace=True) # Removendo a última linha do arquivo
df_planilha_aba1.dropna(subset=['COD_PROCEDIMENTO'], inplace=True) # Removendo linhas com valores nulos
df_planilha_aba1.drop('Unnamed: 7', axis=1, inplace=True) # Removendo coluna 'Unnamed: 7'
df_planilha_aba1['COD_PROCEDIMENTO'] = df_planilha_aba1['COD_PROCEDIMENTO'].astype(int) # Converte a coluna 'COD_PROCEDIMENTO' para string
df_planilha_aba1['PERC_REDUCAO'] = df_planilha_aba1['PERC_REDUCAO'].astype(float) # Converte a coluna 'QUANT_FILA' para string
df_planilha_aba1['QUANT_REDUCAO'] = df_planilha_aba1['QUANT_REDUCAO'].astype(int) # Converte a coluna 'QUANT_REDUCAO' para string
df_planilha_aba1['QUANT_FILA'] = df_planilha_aba1['QUANT_FILA'].astype(int) # Converte a coluna 'QUANT_FILA' para string
print(f"[OK] ABA 1 Planilha carregada:====================> {time.time() - tempo_inicial:.2f} segundos",file=arquivo)

# ABA1 - somas e contagens
quant_fila = df_planilha_aba1['QUANT_FILA'].sum() # Soma o valor total da coluna 'QUANT_FILA'
quant_fila = '{0:,}'.format(quant_fila).replace(',','.') #Aqui coloca os pontos
quant_reducao = df_planilha_aba1['QUANT_REDUCAO'].sum() # Soma o valor total da coluna 'QUANT_REDUCAO'
quant_reducao = '{0:,}'.format(quant_reducao).replace(',','.') #Aqui coloca os pontos
quant_prodedimentos = df_planilha_aba1['COD_PROCEDIMENTO'].count() # Conta a quantidade de procedimentos
reducao_max = df_planilha_aba1['PERC_REDUCAO'].max() # Pega o valor máximo da coluna 'PERC_REDUCAO'
reducao_max = "{:.0f}".format(reducao_max * 100)  # Formata o valor para 2 casas decimais
reducao_min = df_planilha_aba1.loc[df_planilha_aba1['PERC_REDUCAO'] > 0, 'PERC_REDUCAO'].min()
reducao_min = "{:.0f}".format(reducao_min * 100)  # Formata o valor para 2 casas decimais
periodo_atedimento = df_planilha_aba1['TEMPO_MESES'].max() # Pega o valor máximo da coluna 'TEMPO_MESES'
print(f"[OK] ABA 1 Planilha processada:===================> {time.time() - tempo_inicial:.2f} segundos",file=arquivo)

# ABA1 - Verificar duplicidade de procedimentos
df_planilha_aba1['DUPLICADO'] = df_planilha_aba1['COD_PROCEDIMENTO'].duplicated(keep=False)
df_planilha_aba1['M_DUPLICADO'] = np.where(df_planilha_aba1['DUPLICADO'], 'SIM', '-')
df_planilha_aba1.drop('DUPLICADO', axis=1, inplace=True) # Remove a coluna 'DUPLICADO'

# ABA1 - Verificar se o procedimento menor que 1
def mensagem(quant_zero):
    if quant_zero ['QUANT_REDUCAO'] < 1 and quant_zero['PERC_REDUCAO'] > 0 :
        return 'ERRO_QUANT'
    else:
        return '-'
df_planilha_aba1['QUANT_ZERO'] = df_planilha_aba1.apply(mensagem, axis=1)

# ABA1 - Verificar habilitação do procedimento
df_sigtap_h = df_sigtap[['COD_PROCEDIMENTO','EXIGE HABILITACAO','CO_HABILITACAO']] # Cria um novo dataframe com as colunas 'COD_PROCEDIMENTO','EXIGE HABILITACAO','CO_HABILITACAO'
df_sigtap_h.drop_duplicates(subset='COD_PROCEDIMENTO', keep='first', inplace=True) # Remove os valores duplicados da coluna 'COD_PROCEDIMENTO'
df_planilha_aba1['PROC_HABILITACAO'] = df_planilha_aba1['COD_PROCEDIMENTO'].map(df_sigtap_h.set_index('COD_PROCEDIMENTO')['EXIGE HABILITACAO']) # Adiciona uma nova coluna com a informação de habilitação do procedimento

# ABA1 - Verificar serviço do procedimento
df_sigtap_s = df_sigtap[['COD_PROCEDIMENTO','EXIGE SERVIÇO','CO_SERVICO','CO_CLASSIFICACAO']] # Cria um novo dataframe com as colunas 'COD_PROCEDIMENTO','EXIGE SERVICO','CO_SERVICO'
df_sigtap_s.drop_duplicates(subset='COD_PROCEDIMENTO', keep='first', inplace=True) # Remove os valores duplicados da coluna 'COD_PROCEDIMENTO'
df_planilha_aba1['PROC_SERVICO'] = df_planilha_aba1['COD_PROCEDIMENTO'].map(df_sigtap_s.set_index('COD_PROCEDIMENTO')['EXIGE SERVIÇO']) # Adiciona uma nova coluna com a informação de serviço do procedimento
df_planilha_aba1.head() # Exibe as 5 primeiras linhas do arquivo
print(f"[OK] ABA 1 Planilha validada:=====================> {time.time() - tempo_inicial:.2f} segundos",file=arquivo)


## ABA2 - Planilha
df_planilha_aba2 = pd.read_excel(df_planilha, sheet_name='Ident. CNES e Proced.', dtype=str) # Lê o arquivo excel
# Tratamento dos dados da aba 'Ident. CNES e Proced.'
df_planilha_aba2.rename(columns={'PLANO ESTADUAL DE REDUÇÃO DE FILAS DE ESPERA EM CIRURGIAS ELETIVAS - CNES':'CNES','Unnamed: 1':'ESTABELECIMENTO','Unnamed: 2':'COD_PROCEDIMENTO', 
                                 'Unnamed: 3':'DES_PROCEDIMENTO', 'Unnamed: 4':'COMPL_RECURSO_FEDERAL', 'Unnamed: 5':'GESTAO', 'Unnamed: 6':'COD_NATUREZA','Unnamed: 7':'NATUREZA',
                                 'Unnamed: 8':'POSSUI_CONTRATO','Unnamed: 9':'IDENTIFICACAO','Unnamed: 10':'LINHA'}, inplace=True) 
                                # Renomeia a coluna 'PLANO ESTADUAL DE REDUÇÃO DE FILAS DE ESPERA EM CIRURGIAS ELETIVAS - FILA DE ESPERA' para 'UF'
df_planilha_aba2.drop(0, inplace=True) # Remove a primeira linha do arquivo
df_planilha_aba2.drop(1, inplace=True) # Remove a primeira linha do arquivo
df_planilha_aba2.drop(df_planilha_aba2.tail(1).index,inplace=True) # Removendo a última linha do arquivo
df_planilha_aba2.dropna(subset=['CNES'], inplace=True) # Removendo linhas com valores nulos
df_planilha_aba2.drop('IDENTIFICACAO', axis=1, inplace=True) # Removendo coluna 'IDENTIFICACAO'
df_planilha_aba2['COD_PROCEDIMENTO'] = df_planilha_aba2['COD_PROCEDIMENTO'].astype(int) # Converte a coluna 'COD_PROCEDIMENTO' para string
df_cnes_habilitacao = df_cnes_habilitacao.rename(columns={"CO_CNES": "CNES"}) # Renomeia a coluna 'CO_CNES' para 'CNES'
df_planilha_aba2 = df_planilha_aba2.merge(df_cnes_habilitacao[["CNES", "CO_MUNICIPIO_GESTOR"]], on="CNES", how="left") # Adiciona a coluna 'CO_MUNICIPIO_GESTOR' ao dataframe
print(f"[OK] ABA 2 Planilha carregada:====================> {time.time() - tempo_inicial:.2f} segundos",file=arquivo)


# ABA2 - Verificar CNES ATIVO
df_cnes_habilitacao['CNES'] = df_cnes_habilitacao['CNES'].astype(str) # Converte a coluna 'CNES' para string
df_cnes_habilitacao2 = df_cnes_habilitacao.loc[df_cnes_habilitacao['CO_MOTIVO_DESAB'] > '0'] # Seleciona apenas os CNES habilitados
df_planilha_aba2['CNES_ATIVO'] = np.where(df_planilha_aba2['CNES'].isin(df_cnes_habilitacao2['CNES']), 'NÃO', '-') # Adiciona a coluna 'CNES_ATIVO' ao dataframe

# ABA2 - Verificar com a aba 1
df_planilha_aba2['PROC_INFORMADO'] = np.where(df_planilha_aba2['COD_PROCEDIMENTO'].isin(df_planilha_aba1['COD_PROCEDIMENTO']), '-','NÃO')     
df_planilha_aba1_p = df_planilha_aba1.loc[df_planilha_aba1['QUANT_REDUCAO'] > 0] # Seleciona apenas os procedimentos com quantidade de redução maior que zero
df_planilha_aba1_p['POSSUI_PRESTADOR'] = np.where(df_planilha_aba1_p['COD_PROCEDIMENTO'].isin(df_planilha_aba2['COD_PROCEDIMENTO']),'SIM','NÃO')
df_planilha_aba1 = df_planilha_aba1.merge(df_planilha_aba1_p[['COD_PROCEDIMENTO','POSSUI_PRESTADOR']], on='COD_PROCEDIMENTO', how='left') # Adiciona a coluna 'POSSUI_PRESTADOR' ao dataframe

# ABA2 - Verificar procedimento válido
df_planilha_aba1['PROC_VALIDO'] = np.where(df_planilha_aba1['COD_PROCEDIMENTO'].isin(df_sigtap['COD_PROCEDIMENTO']), '-','NÃO')


# ABA2 - Verificar habilitação e CNES
df_planilha_aba2_h = df_planilha_aba2[['CNES','COD_PROCEDIMENTO']] # Cria um novo dataframe com as colunas 'CNES','COD_PROCEDIMENTO',
df_planilha_aba2_h.drop_duplicates(subset='COD_PROCEDIMENTO', keep='first', inplace=True) # Remove os valores duplicados da coluna 'COD_PROCEDIMENTO'
df_planilha_aba2_h['PROC_HABILITACAO'] = df_planilha_aba2_h['COD_PROCEDIMENTO'].map(df_sigtap_h.set_index('COD_PROCEDIMENTO')['EXIGE HABILITACAO']) # Adiciona uma nova coluna com a informação de habilitação do procedimento
df_planilha_aba2_h = df_planilha_aba2_h.merge(df_sigtap_h[['COD_PROCEDIMENTO','CO_HABILITACAO']], on='COD_PROCEDIMENTO', how='left') # Adiciona a coluna 'PROC_VALIDO' ao dataframe
df_planilha_aba2_h = df_planilha_aba2_h.merge(df_cnes_habilitacao[['CNES','CO_CODIGO_GRUPO']], on='CNES', how='left') # Adiciona a coluna 'PROC_VALIDO' ao dataframe
df_planilha_aba2_h.drop(df_planilha_aba2_h.loc[df_planilha_aba2_h['PROC_HABILITACAO'] == '-'].index, inplace=True) # Remove os procedimentos que não exigem habilitação
df_planilha_aba2_h['CNES_HABILITADO'] = np.where(df_planilha_aba2_h['CO_CODIGO_GRUPO'].isin(df_planilha_aba2_h['CO_HABILITACAO']), 'SIM','EXIGE_HAB') # Adiciona a coluna 'CNES_HABILITADO' ao dataframe
df_planilha_aba2_h.drop_duplicates(subset='COD_PROCEDIMENTO', keep='first', inplace=True) # Remove os valores duplicados da coluna 'CNES'
df_planilha_aba2 = df_planilha_aba2.merge(df_planilha_aba2_h[['CNES','COD_PROCEDIMENTO','CNES_HABILITADO']], on=['CNES','COD_PROCEDIMENTO'], how='left') # Adiciona a coluna 'CNES_HABILITADO' ao dataframe
df_planilha_aba2.drop_duplicates(subset='LINHA', keep='first', inplace=True) # Remove os valores duplicados da coluna 'CNES'
print(f"[OK] ABA 2 Planilha processando:==================> {time.time() - tempo_inicial:.2f} segundos",file=arquivo)

# ABA2 - Verificar serviço/class e CNES
df_planilha_aba2_s = df_planilha_aba2[['CNES','COD_PROCEDIMENTO']] # Cria um novo dataframe com as colunas 'CNES','COD_PROCEDIMENTO',
df_planilha_aba2_s.drop_duplicates(subset='COD_PROCEDIMENTO', keep='first', inplace=True) # Remove os valores duplicados da coluna 'COD_PROCEDIMENTO'
df_planilha_aba2_s['EXIGE SERVIÇO'] = df_planilha_aba2_s['COD_PROCEDIMENTO'].map(df_sigtap_s.set_index('COD_PROCEDIMENTO')['EXIGE SERVIÇO']) # Adiciona uma nova coluna com a informação de habilitação do procedimento
df_planilha_aba2_s = df_planilha_aba2_s.merge(df_sigtap_s[['COD_PROCEDIMENTO','CO_SERVICO']], on='COD_PROCEDIMENTO', how='left') # Adiciona a coluna 'PROC_VALIDO' ao dataframe
df_cnes_servicos = df_cnes_servicos.rename(columns={"CO_CNES": "CNES"}) # Renomeia a coluna 'CO_CNES' para 'CNES'
df_planilha_aba2_s = df_planilha_aba2_s.merge(df_cnes_servicos[['CNES','CO_SERVICO']], on='CNES', how='left') # Adiciona a coluna 'PROC_VALIDO' ao dataframe
df_planilha_aba2_s.drop(df_planilha_aba2_s.loc[df_planilha_aba2_s['EXIGE SERVIÇO'] == '-'].index, inplace=True) # Remove os procedimentos que não exigem habilitação
df_planilha_aba2_s['CNES_SERVICO'] = np.where(df_planilha_aba2_s['CO_SERVICO_x'].isin(df_planilha_aba2_s['CO_SERVICO_y']), 'SIM','EXIGE_SERV') # Adiciona a coluna 'CNES_HABILITADO' ao dataframe
df_planilha_aba2_s.drop_duplicates(subset='COD_PROCEDIMENTO', keep='first', inplace=True) # Remove os valores duplicados da coluna 'CNES'
df_planilha_aba2 = df_planilha_aba2.merge(df_planilha_aba2_s[['CNES','COD_PROCEDIMENTO','CNES_SERVICO']], on=['CNES','COD_PROCEDIMENTO'], how='left') # Adiciona a coluna 'CNES_HABILITADO' ao dataframe
df_planilha_aba2.drop_duplicates(subset='LINHA', keep='first', inplace=True) # Remove os valores duplicados da coluna 'CNES'

# ABA2 - somas e contagens
quant_cnes = df_planilha_aba2['CNES'].nunique() # Quantidade de CNES
quant_cnes_municipal = df_planilha_aba2['CNES'].loc[df_planilha_aba2['GESTAO'] == 'MUNICIPAL'].nunique() # Quantidade de municípios
quant_cnes_estadual = df_planilha_aba2['CNES'].loc[df_planilha_aba2['GESTAO'] == 'ESTADUAL'].nunique() # Quantidade de estadual
print(f"[OK] ABA 2 Planilha validada:=====================> {time.time() - tempo_inicial:.2f} segundos",file=arquivo)


# ABA3 - Verificar procedimento
df_planilha_aba3 = pd.read_excel(df_planilha, sheet_name='Execução') # Lê o arquivo excel
valor_portaria = df_planilha_aba3.iloc[0,3] # Armazena o valor da portaria
df_planilha_aba3.drop(df_planilha_aba3.index[0:6], inplace=True) # Remove as 5 primeiras linhas do arquivo
df_planilha_aba3.rename(columns={'Distribuição e Cronograma da Execução do Recurso Financeiro':'CODIGO GESTOR','Unnamed: 1':'GESTÃO','Unnamed: 2':'DESC_GESTOR','Unnamed: 3':'VALOR','Unnamed: 4':'MARÇO',
                                 'Unnamed: 5':'ABRIL','Unnamed: 6':'MAIO','Unnamed: 7':'JUNHO','Unnamed: 8':'JULHO','Unnamed: 9':'AGOSTO','Unnamed: 10':'SETEMBRO','Unnamed: 11':'OUTUBRO',
                                 'Unnamed: 12':'NOVEMBRO','Unnamed: 13':'DEZEMBRO','Unnamed: 14':'TOTAL_%','SQ (CODIGO Interno':'LINHA'}, inplace=True)
df_planilha_aba3.drop(df_planilha_aba3.tail(1).index,inplace=True) # Removendo a última linha do arquivo
df_planilha_aba3.dropna(subset=['CODIGO GESTOR'], inplace=True) # Removendo linhas com valores nulos
valor_total = df_planilha_aba3['VALOR'].sum() # Soma o valor total da coluna 'VALOR'
df_planilha_aba3['VALOR'] = df_planilha_aba3['VALOR'].astype(float) # Converte a coluna 'VALOR' para float
df_planilha_aba3['VALOR_R'] = df_planilha_aba3['VALOR'].apply(lambda x: 'R$ ' + format(x, ',.2f').replace('.', '#').replace(',', '.').replace('#', ',')) # Formata a coluna 'VALOR' para moeda
print(f"[OK] ABA 3 Planilha carregada:====================> {time.time() - tempo_inicial:.2f} segundos",file=arquivo)

# ABA3 - Verificar higienização
df_planilha_aba3['CODIGO GESTOR'] = df_planilha_aba3['CODIGO GESTOR'].astype(int) # Converte a coluna 'MUNIC_PRESTADOR' para string
df_planilha_aba2['CO_MUNICIPIO_GESTOR'] = df_planilha_aba2['CO_MUNICIPIO_GESTOR'].astype(int) # Converte a coluna 'CO_MUNICIPIO_GESTOR' para string
df_planilha_aba3['MUNIC_PRESTADOR'] = np.where(df_planilha_aba3['CODIGO GESTOR'].isin(df_planilha_aba2['CO_MUNICIPIO_GESTOR']), 'SIM','NÃO')
df_planilha_aba3_m = df_planilha_aba3[df_planilha_aba3['GESTÃO'] == 'MUNICIPAL'] # Filtra os dados da aba 3 que possuem gestão municipal
df_teto['Código IBGE'] = df_teto['Código IBGE'].astype(int) # Converte a coluna 'Código IBGE' para string
df_planilha_aba3 = pd.merge(df_planilha_aba3, df_teto, left_on='CODIGO GESTOR', right_on='Código IBGE', how='left') # Realiza o merge das duas planilhas

df_planilha_aba3.drop(['Código IBGE', 'Código Gestão', 'Descrição Gestão'], axis=1, inplace=True) # Remove a coluna 'Código IBGE'
df_planilha_aba3.rename(columns={'Descrição Gestão':'DESC_GESTOR','Estado / Município':'DESC_GESTOR_C','Teto Financeiro MAC - Valores Anuais (R$)':'TETO_FINANC_ANO'}, inplace=True) # Renomeia a coluna 'Descrição Gestão'
df_planilha_aba3['TETO_FINANC_ANO'] = df_planilha_aba3['TETO_FINANC_ANO'].astype(float) # Converte a coluna 'TETO_FINANC_ANO' para float
df_planilha_aba3['TETO_FINANC_MES'] = df_planilha_aba3['TETO_FINANC_ANO'] / 12 # Calcula o teto financeiro mensal
df_planilha_aba3.dropna(subset=['DESC_GESTOR'], inplace=True) # Remove as linhas com valores nulos

df_planilha_aba3['VALOR'] = df_planilha_aba3['VALOR'].astype(float) # Converte a coluna 'VALOR' para float
df_planilha_aba3['VALOR'] = df_planilha_aba3['VALOR'].apply(lambda x: 'R$ ' + format(x, ',.2f').replace('.', '#').replace(',', '.').replace('#', ',')) # Formata a coluna 'VALOR' para moeda
df_planilha_aba3['TETO_FINANC_ANO'] = df_planilha_aba3['TETO_FINANC_ANO'].astype(float) # Converte a coluna 'TETO_FINANC_MES' para float
df_planilha_aba3['TETO_FINANC_ANO'] = df_planilha_aba3['TETO_FINANC_ANO'].apply(lambda x: 'R$ ' + format(x, ',.2f').replace('.', '#').replace(',', '.').replace('#', ',')) # Formata a coluna 'TETO_FINANC_MES' para moeda
df_planilha_aba3['TETO_FINANC_MES'] = df_planilha_aba3['TETO_FINANC_MES'].astype(float) # Converte a coluna 'TETO_FINANC_MES' para float
df_planilha_aba3['TETO_FINANC_MES'] = df_planilha_aba3['TETO_FINANC_MES'].apply(lambda x: 'R$ ' + format(x, ',.2f').replace('.', '#').replace(',', '.').replace('#', ',')) # Formata a coluna 'TETO_FINANC_MES' para moeda

cols = ['MARÇO','ABRIL','MAIO','JUNHO','JULHO','AGOSTO','SETEMBRO','OUTUBRO','NOVEMBRO','DEZEMBRO','TOTAL_%'] # Lista de colunas
df_planilha_aba3[cols] = df_planilha_aba3[cols].fillna(0).astype(float) # Converte os valores para float
df_planilha_aba3[cols] = df_planilha_aba3[cols].applymap(lambda x: '{:.0%}'.format(float(x))) # Formata as colunas para porcentagem
print(f"[OK] ABA 3 Planilha processada:===================> {time.time() - tempo_inicial:.2f} segundos",file=arquivo)

# ABA3 - Gestão Municipal x execução
df_planilha_aba2_e = df_planilha_aba2[['CNES','GESTAO','CO_MUNICIPIO_GESTOR']] # Filtra as colunas 'CNES' e 'GESTAO' da aba 2
df_planilha_aba2_e.drop(df_planilha_aba2_e.loc[df_planilha_aba2_e['GESTAO']!='MUNICIPAL'].index, inplace=True) # Remove as linhas que possuem gestão municipal
df_planilha_aba2_e = df_planilha_aba2_e.drop_duplicates() # Remove as linhas duplicadas
df_planilha_aba2_e['CNES GESTÃO MUNIC_X EXECUÇÃO'] = np.where(df_planilha_aba2_e['CO_MUNICIPIO_GESTOR'].isin(df_planilha_aba3['CODIGO GESTOR']), '-','NÃO') # Verifica se o CNES da aba 2 está na aba 3
df_planilha_aba2 = df_planilha_aba2.merge(df_planilha_aba2_e[['CNES','CNES GESTÃO MUNIC_X EXECUÇÃO']], on='CNES', how='left') # Realiza o merge das duas planilhas

# ABA3 - somas e contagens
valor_portaria = round(valor_portaria, 2) # Arredonda o valor da portaria para duas casas decimais
valor_total = round(valor_total, 2) # Arredonda o valor total para duas casas decimais

diferenca = valor_portaria - valor_total # Calcula a diferença entre o valor da portaria e o valor total
valor_total = 'R$ ' + format(valor_total, ',.2f').replace('.', '#').replace(',', '.').replace('#', ',') # Formata o valor total para moeda

## FINALIZAÇÃO
# Salvar arquivo
df_planilha = os.path.splitext(os.path.basename(df_planilha))[0] # Pega o nome do arquivo sem a extensão
file_nome = df_planilha.split('/')[-1] # Pega o nome do arquivo
writer = pd.ExcelWriter(f'RESULTADOS/{file_nome}_resultado.xlsx', engine='xlsxwriter') # Cria um arquivo excel
df_planilha_aba1.to_excel(writer, sheet_name='Aba 1', index=False)
df_planilha_aba2.to_excel(writer, sheet_name='Aba 2', index=False)
df_planilha_aba3.to_excel(writer, sheet_name='Aba 3', index=False)
writer.save()

#Criar arquivo txt resultado em modo de escrita
#arquivo = open(f'RESULTADOS/{file_nome}_resultado.txt', 'w')


# Informações do arquivo
print(f"\n \n \n ================================ INFORMAÇÕES DO ARQUIVO ========================= \n \n", file=arquivo)

# Verificação de procedimentos duplicados
if df_planilha_aba1['M_DUPLICADO'].str.contains('SIM').any():
    print(f"[ERRO] - ABA 1 - Existem procedimentos na Fila, duplicado;", file=arquivo)
    procedimento_duplicado = True
else:
    print(f" [OK] - ABA 1 - Não existem procedimentos duplicados;", file=arquivo)
    procedimento_duplicado = False


# VerificaçãO de procedimentos com quantidade menor que 1
if df_planilha_aba1['QUANT_ZERO'].str.contains('ERRO_QUANT').any():   
    print(f" [ERRO] - ABA 1 - Existem procedimentos na Fila, cuja quantidade de cirurgia ficou inferior a 1 procedimento (PACIENTE);", file=arquivo)
    quant_menor_1 = True
else:
    print(f" [OK] - ABA 1 - Não existem procedimentos com quantidade menor que 1;", file=arquivo)
    quant_menor_1 = False


# Verificar porcentagem  de procedimentos com quantidade 
if df_planilha_aba1['PERC_REDUCAO'].apply(lambda x: x > 1).any():
    print(f" [ERRO] - ABA 1 - Existem procedimentos na Fila com mais de 100% de redução;", file=arquivo)
    quant_menor_1 = True
else:
    print(f" [OK] - ABA 1 - Não existem procedimentos na Fila com mais de 100% de redução;", file=arquivo)
    quant_menor_1 = False


# Verificação de procedimentos inválidos
if df_planilha_aba1['PROC_VALIDO'].str.contains('NÃO').any():
    print(f" [ERRO] - ABA 1 - Existem procedimentos na Fila, que não são válidos;", file=arquivo)
    procedimento_invalido = True
else:
    print(f" [OK] - ABA 1 - Não existem procedimentos inválidos;", file=arquivo)
    procedimento_invalido = False    


# Verificação de procedimentos sem prestador
if df_planilha_aba1['POSSUI_PRESTADOR'].str.contains('NÃO').any():
    print(f" [ERRO] - ABA 1/2 - Existem procedimentos na Fila, cuja não existe prestador;", file=arquivo)
    sem_prestador = True
else:
    print(f" [OK] - ABA 1/2 - Não existem procedimentos sem prestador;", file=arquivo)
    sem_prestador = False


# Verificação de prestadores sem procedimento
if df_planilha_aba2['PROC_INFORMADO'].str.contains('NÃO').any():
    print(f" [ERRO] - ABA 2/1 - Existem prestador na Fila, que não possuem procedimentos;", file=arquivo)
    sem_procedimento = True
else:
    print(f" [OK] - ABA 2/1 - Não existem prestadores sem procedimentos;", file=arquivo)
    sem_procedimento = False


# Verificação de CNES ativo
if df_planilha_aba2['CNES_ATIVO'].str.contains('NÃO').any():
    print(f" [ERRO] - ABA 2 - Existem CNES inativos;", file=arquivo)
    cnes_inativo = True
else:
    print(f" [OK] - ABA 2 - Não existem CNES inativos;", file=arquivo)
    cnes_inativo = False


# Verificação de CNES habilitado
if df_planilha_aba2['CNES_HABILITADO'].str.contains('EXIGE_HAB').any():
    print(f" [ALERTA] - ABA 2 - Existem CNES não habilitados;", file=arquivo)
    cnes_nao_habilitado = True
else:
    print(f" [OK] - ABA 2 - Não existem CNES não habilitados;", file=arquivo)
    cnes_nao_habilitado = False


# Verificação de CNES serviço ativo
if df_planilha_aba2['CNES_SERVICO'].str.contains('EXIGE_SERV').any():
    print(f" [ALERTA] - ABA 2 - Existem CNES não serviço/class;", file=arquivo)
    cnes_nao_serv_class = True
else:
    print(f" [OK] - ABA 2 - Não existem CNES não serviço/class;", file=arquivo)
    cnes_nao_serv_class = False

# CNES GESTÃO MUNIC_X EXECUÇÃO
if df_planilha_aba2['CNES GESTÃO MUNIC_X EXECUÇÃO'].str.contains('NÃO').any():
    print(f" [ERRO] - ABA 2 - Existem CNES de gestão municipal não relacionado na ABA 3;", file=arquivo)
    cnes_gestao_mun = True  
else:
    print(f" [OK] - ABA 2 - CNES de gestão municipal relacionado na ABA3;", file=arquivo)
    cnes_gestao_mun = False


# Verificar valor de portaria
if diferenca == 0:
    print(f" [OK] - ABA 3 - Valor programado igual ao valor alocado na Portaria 90;", file=arquivo)
    valor_portaria_correto = True
else:   
    print(f" [ERRO] - ABA 3 - Valor programado diferente do valor alocado na Portaria 90; {diferenca}", file=arquivo)
    valor_portaria_correto = False
    

# Verificar se existe município com repasse, mas não existe CNES relacionado ao municipio
if df_planilha_aba3_m['MUNIC_PRESTADOR'].str.contains('NÃO').any():   
    print(f" [ERRO] - ABA 3 - Existem municipio com repasse, mas não existe CNES relacionado ao município;", file=arquivo)
    
    sem_prestador = True
else:   
    print(f" [OK] - ABA 3 - Relação de município desacordo com o CNES;", file=arquivo)
    sem_prestador = False


# Arquivo gerado com os resultados
print(f" [OK] - Arquivo: '{file_nome}- resultado.xlsx' gerado com sucesso!", file=arquivo)


# RESULTADO FINAL
print(f"\n \n \n \n ================================ RESULTADO FINAL ================================ \n", file=arquivo)
print(f" QUANTIDADE DE SOLICITAÇÕES NA FILA ATÉ DIA 31/12/22 =====> {quant_fila}", file=arquivo)
print(f" QTDE DE CIRURGIAS A SEREM FEITAS NO PRAZO PACTUADO  =====> {quant_reducao}", file=arquivo)
print(f" QTDE PROCEDIMENTO CIRURGICOS INFORMADO NA FILA   ========> {quant_prodedimentos}", file=arquivo)
print(f" REDUÇÃO DO TAMANHO DA FILA (%) - MAX e MIN ==============> {reducao_max}% e {reducao_min}%", file=arquivo)
print(f" PRAZO PARA OS ATENDIMENTOS ==============================> {periodo_atedimento} meses", file=arquivo)
print(f" TOTAL DE ESTABELECIMENTOS CNES ==========================> {quant_cnes}", file=arquivo)
print(f" TOTAL DE ESTABELECIMENTOS EM GESTÃO MUNICIPAL ===========> {quant_cnes_municipal}", file=arquivo)
print(f" TOTAL DE ESTABELECIMENTOS EM GESTÃO ESTADUAL ============> {quant_cnes_estadual}", file=arquivo)
print(f" VALOR TOTAL ALOCADO NA PORTARIA 90 ======================> {valor_total}", file=arquivo)

# Tempo de execução
print(f" [TEMPO] Tempo total de execução: {time.time() - tempo_inicial:.2f} segundos",file=arquivo)

# Fechar arquivo txt
arquivo.close()

print(f"[OK] Fim do código:===============================> {time.time() - tempo_inicial:.2f} segundos")