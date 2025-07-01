import os

# Definir o caminho da pasta
pasta = r"C:\Users\ESTAGIO CONSULTORIA\Desktop\Planilhas Bussula"  # Substitua pelo caminho real

# Obter a lista de arquivos na pasta
arquivos = os.listdir(pasta)
for i in range(1,5):
    arquivos.pop(-1)

print(arquivos)


