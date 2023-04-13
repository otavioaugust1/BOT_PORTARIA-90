# BOT_PORTARIA-90

# BOT para Avaliação de Planilhas - Portaria 90

Este BOT foi desenvolvido em Python para avaliar planilhas enviadas de acordo com a PORTARIA GM/MS Nº 90, DE 03 DE FEVEREIRO DE 2023 – INSTITUI O PROGRAMA NACIONAL DE REDUÇÃO DAS FILAS DE CIRURGIAS ELETIVAS. Ele é capaz de analisar os dados enviados e verificar se estão em conformidade com as exigências da portaria.

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
* zipfile
* os
* re
* ftplib
* urllib 
* XlsxWriter
* glob
* Time
* warnings
* pyexcel
* locale
* math

## Como utilizar
Para utilizar o BOT, basta seguir os seguintes passos:

1. Clonar o repositório em sua máquina:
```
git clone https://github.com/otavioaugust1/BOT_PORTARIA-90
```

2. Instalar as bibliotecas necessárias:
```
pip install pandas numpy openpyxl glob time XlsxWriter zipfile os re ftplib urllib pyexcel locale math
```

3. Executar o BOT gerar BASE:
```
python tratamento_base.py
ou jupyter notebook tratamento_base.ipynb
```

4. Coloque a planilha a ser avaliada na pasta "PLANILHA" e

5. Executar o BOT verificador:
```
juptyer notebook validador.ipynb
```

6. Analisar os resultados da avaliação e o relatório gerado pelo BOT na pasta "RESULTADOS".

7. Enviar notificações sobre a avaliação conforme necessário.


## Observações
* O BOT foi desenvolvido com base nas exigências da Portaria 90 vigente até setembro de 2021. Caso haja alguma alteração na portaria, é necessário atualizar o código do BOT para refletir as mudanças.
* O BOT foi desenvolvido apenas para fins de avaliação de planilhas e não substitui a análise humana em relação aos dados enviados.
* Caso haja dúvidas sobre o uso do BOT ou sobre a avaliação de planilhas, favor entrar em contato com o responsável pelo projeto.



