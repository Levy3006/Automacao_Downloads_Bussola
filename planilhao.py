import pandas as pd
import os 
# Lista de arquivos # Definir o caminho da pasta
p = r"C:\Users\ESTAGIO CONSULTORIA\Desktop\Planilhas Bussula\pConcatenadas"  # Substitua pelo caminho real

# Obter a lista de arquivos na pasta
arquivos = os.listdir(p)

dfs = []
# Carregar todas as planilhas em uma lista de DataFrames
for arquivo in arquivos:
    caminho_completo = os.path.join(p, arquivo)  # Junta a pasta com o nome do arquivo
    if arquivo.endswith(".xlsx"):  # Garante que é um Excel
        df = pd.read_excel(caminho_completo)
        dfs.append(df)



# Obter todas as colunas únicas presentes em qualquer DataFrame
todas_colunas = set().union(*[df.columns for df in dfs])

# Garantir que todos os DataFrames tenham as mesmas colunas
for df in dfs:
    for coluna in todas_colunas:
        if coluna not in df.columns:
            print('==== faltou colunas ==== ')
            df[coluna] = None  # Adiciona a coluna ausente com valores vazios

df_final = pd.concat(dfs, ignore_index=True)

df_final.to_excel('Novo Planilhão Final.xlsx',index=False)
print('===== plnilhão criado com sucesso =====')