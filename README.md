# BOT_PORTARIA-90

# BOT para Avaliação de Planilhas - Portaria 90

Este BOT foi desenvolvido em Python para avaliar planilhas enviadas de acordo com a Portaria 90. Ele é capaz de analisar os dados enviados e verificar se estão em conformidade com as exigências da portaria.

## Funcionalidades

O BOT possui as seguintes funcionalidades:

* Leitura de planilhas em formato Excel
* Verificação de dados obrigatórios conforme Portaria 90
* Cálculo de indicadores de desempenho
* Geração de relatórios de avaliação
* Envio de notificações sobre a avaliação

## Requisitos
Para utilizar o BOT, é necessário ter as seguintes bibliotecas instaladas:

* Pandas
* NumPy
* OpenPyXL

## Dados Externo 

1. Realizar donwload no site CNES:
* http://cnes.saude.gov.br/pages/downloads/arquivosBaseDados.jsp 
* selecione o arquivo mais recente e coloque na pasta 'BASE'

2. Realizar donwload no site SIGTAP
* http://sigtap.datasus.gov.br/tabela-unificada/app/download.jsp 
* selecione o arquivo mais recente e coloque na pasta 'BASE'

3. Realizar donwload no site SISMAC
* https://sismac.saude.gov.br/teto_financeiro_brasil 
* selecione o arquivo mais recente e coloque na pasta 'BASE'

## Como utilizar
Para utilizar o BOT, basta seguir os seguintes passos:

1. Clonar o repositório em sua máquina:
```
git clone https://github.com/seu-usuario/nome-do-repositorio.git
```

2. Instalar as bibliotecas necessárias:
```
pip install pandas numpy openpyxl
```

3. Executar o BOT:
```
python bot.py
```

4. Selecionar a planilha a ser avaliada."PLANILHA"
5. Analisar os resultados da avaliação e o relatório gerado pelo BOT.
6. Enviar notificações sobre a avaliação conforme necessário.


## Observações
* O BOT foi desenvolvido com base nas exigências da Portaria 90 vigente até setembro de 2021. Caso haja alguma alteração na portaria, é necessário atualizar o código do BOT para refletir as mudanças.
* O BOT foi desenvolvido apenas para fins de avaliação de planilhas e não substitui a análise humana em relação aos dados enviados.
* Caso haja dúvidas sobre o uso do BOT ou sobre a avaliação de planilhas, favor entrar em contato com o responsável pelo projeto.



