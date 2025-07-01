import pandas as pd
from obterNomes import arquivos

def concatenar_abas(nome_arquivo):
    global pd
    #nome_arquivo = '01_2025 - BÚSSOLA - (LOJA 01) FARMANOSSA PRODUTOS FARMACEUTICOS LTDA FILIAL 02 - 16366691000343.xlsx'
    df = pd.read_excel(nome_arquivo, sheet_name=['NÃO_MEDICAMENTO','PROPAGADO','SIMILAR','GENÉRICO'],skiprows=9)
    cnpj = nome_arquivo.split('-')[3].removesuffix('.xlsx').strip()
    p1 = df['NÃO_MEDICAMENTO']
    p2 = df['PROPAGADO']
    p3 = df['SIMILAR']
    p4 = df['GENÉRICO']

    # Lista de arquivos das planilhas
    arquivos = [p1,p2,p3,p4]

    # Carregar todas as planilhas em uma lista de DataFrames
    dfs = [arquivo for arquivo in arquivos]

    # Obter todas as colunas únicas presentes em qualquer DataFrame
    todas_colunas = set().union(*[df.columns for df in dfs])

    # Garantir que todos os DataFrames tenham as mesmas colunas
    for df in dfs:
        for coluna in todas_colunas:
            if coluna not in df.columns:
                df[coluna] = None  # Adiciona a coluna ausente com valores vazios

    df_final = pd.concat(dfs, ignore_index=True)
    # Deletar a primeira coluna pelo índice
    df_final = df_final.iloc[:, 1:]
    nome_planilha = f'planilha_{cnpj}.xlsx'

    df_final.to_excel(nome_planilha, index=False)
    return f'====== {nome_planilha} criada com sucesso ======'

for i in arquivos:
    concatenar_abas(i)
else:
    print('=== todos os arquivos doram concatenados com sucesso! ===')