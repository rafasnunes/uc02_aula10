import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

try:
    print("Obtendo dados...")
    ENDERECO_DADOS = "https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv"

    # Buscar a base de dados CSV online do site ISP (Instituto de Segurança Pública)
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')

    df_ocorrencias.loc[df_ocorrencias['regiao'].str.contains('Grande Niter', na=False), 'regiao'] = 'Grande Niterói'
    # print(df_ocorrencias)

    # Delimitando as variáveis
    # df_roubo_veiculo = df_ocorrencias[['regiao', 'munic', 'roubo_veiculo']]
    df_roubo_veiculo = df_ocorrencias[['regiao', 'cisp', 'roubo_veiculo']]

    # Agrupando
    # df_roubo_veiculo = df_roubo_veiculo.groupby(['regiao', 'munic']).sum(['roubo_veiculo']).reset_index()
    df_roubo_veiculo = df_roubo_veiculo.groupby(['regiao', 'cisp']).sum(['roubo_veiculo']).reset_index()

    df_regiao = df_roubo_veiculo[df_roubo_veiculo['regiao'] == 'Capital']

    print(df_regiao)

except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()

try:
    array_roubo_veiculo = np.array(df_regiao['roubo_veiculo'])

    media_roubo_veiculo = np.mean(array_roubo_veiculo)
    mediana_roubo_veiculo = np.median(array_roubo_veiculo)
    distancia_media_mediana = abs(media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo

    # Quartis
    q1 = np.quantile(array_roubo_veiculo, 0.25)
    q2 = np.quantile(array_roubo_veiculo, 0.50)
    q3 = np.quantile(array_roubo_veiculo, 0.75)
    
    # IQR
    iqr = q3 - q1

    # limite inferior
    limite_inferior = q1 - (iqr * 1.5)

    # limite superior
    limite_superior = q3 + (iqr * 1.5)


    # ***** IMPLEMENTAR AS LINHAS (ROUBOS MAIS E MENOS) *****
    # menores roubos
    df_roubo_veiculo_menores = df_regiao[df_regiao['roubo_veiculo'] < q1]

    # maiores roubos
    df_roubo_veiculo_maiores = df_regiao[df_regiao['roubo_veiculo'] > q3]

    # Medidas de dispersão
    maximo = np.max(array_roubo_veiculo)
    minimo = np.min(array_roubo_veiculo)
    amplitude_total = maximo - minimo

    variancia = np.var(array_roubo_veiculo)
    distancia_variancia_media = variancia / (media_roubo_veiculo ** 2)
    desvio_padrao = np.std(array_roubo_veiculo)
    coeficiente_variacao = desvio_padrao / media_roubo_veiculo

    assimetria = df_regiao['roubo_veiculo'].skew()
    curtose = df_regiao['roubo_veiculo'].kurtosis()
    
    # ***** IMPLEMENTAR AS LINHAS (OUTLIERS MAIORES E MENORES) *****
    # outliers inferiores
    df_roubo_veiculo_outliers_inferiores = df_regiao[df_regiao['roubo_veiculo'] < limite_inferior]
    # outiliers superiores
    df_roubo_veiculo_outliers_superiores = df_regiao[df_regiao['roubo_veiculo'] > limite_superior]


    # MEDIDAS
    print("\nMEDIAS DE TENDÊNCIA CENTRAL")
    print(f'Média: {media_roubo_veiculo}')
    print(f'Mediana: {mediana_roubo_veiculo}')
    print(f'Distância entre média e mediana: {distancia_media_mediana}')

    # QUARTIS
    print("\nQUARTIS")
    print(f'Q1: {q1}')
    print(f'Q2: {q2}')
    print(f'Q3: {q3}')
    print(f'IQR: {iqr}')
    print(f'Limite inferior: {limite_inferior}')
    print(f'Limite superior: {limite_superior}')

    # MEIDADAS DE DISPERSÃO
    print("\nMEDIDAS DE DISPERSÃO")
    print(f'Máximo: {maximo}')
    print(f'Mínimo: {minimo}')
    print(f'Amplitude total: {amplitude_total}')
    print(f'Variancia: {variancia}')
    print(f'Distância entre variância e média: {distancia_variancia_media}')
    print(f'Desvio padrão: {desvio_padrao}')
    print(f'Coeficiente de variação: {coeficiente_variacao}')

    # MEIDADAS DE DISTRIBUIÇÃO
    print('\nMEDIDAS DE DISTRIBUIÇÃO: ')
    print(30*'-')
    print(f'Assimetria: {assimetria}')
    print(f'Curtose: {curtose}')


    # MAIORES E MENORES ROUBOS
    print("\nMENORES ROUBOS")
    print(df_roubo_veiculo_menores.sort_values(by='roubo_veiculo', ascending=True))
    print("\nMAIORES ROUBOS")
    print(df_roubo_veiculo_maiores.sort_values(by='roubo_veiculo', ascending=False))
    
    # OUTLIERS
    # OUTLIERS INFERIORES
    print("\nOUTLIERS INFERIORES")
    if len(df_roubo_veiculo_outliers_inferiores) > 0:
        print(df_roubo_veiculo_outliers_inferiores.sort_values(by='roubo_veiculo', ascending=False))
    else:
        print("Não há outliers inferiores")
    
    # OUTLIERS SUPERIORES
    print("\nOUTLIERS SUPERIORES")
    if len(df_roubo_veiculo_outliers_superiores) > 0:
        print(df_roubo_veiculo_outliers_superiores.sort_values(by='roubo_veiculo', ascending=False))
    else:
        print("Não há outliers superiores")

except Exception as e:
    print(f"Erro ao obter dados: {e}")
    exit()