import os
import shutil

def renomear_arquivos(pasta):
    # Percorre todos os arquivos na pasta
    for arquivo in os.listdir(pasta):
        caminho_arquivo_antigo = os.path.join(pasta, arquivo)
        if os.path.isfile(caminho_arquivo_antigo) and arquivo.endswith('.txt'):
            # Renomeia o arquivo removendo espaços e convertendo para minúsculas
            novo_nome = arquivo.replace(' ', '').lower()
            caminho_arquivo_novo = os.path.join(pasta, novo_nome)
            os.rename(caminho_arquivo_antigo, caminho_arquivo_novo)

            # Cria a pasta com base nos últimos dois caracteres antes de ".txt"
            pasta_nome = novo_nome[-10:-4]
            pasta_caminho = os.path.join(os.getcwd(), 'arquivos_divididos', pasta_nome)
            if not os.path.exists(pasta_caminho):
                os.makedirs(pasta_caminho)

            # Move o arquivo renomeado para a pasta
            shutil.move(caminho_arquivo_novo, os.path.join(pasta_caminho, novo_nome))

        elif os.path.isdir(caminho_arquivo_antigo):
            # Se for uma pasta, chama recursivamente a função para processar a subpasta
            renomear_arquivos(caminho_arquivo_antigo)

# Diretório raiz onde está a pasta "origem"
diretorio_raiz = os.getcwd()

# Caminho da pasta "origem"
pasta_origem = os.path.join(diretorio_raiz, 'arquivos')

# Verifica se a pasta "origem" existe
if os.path.exists(pasta_origem):
    # Chama a função para renomear os arquivos
    renomear_arquivos(pasta_origem)
    print("Operações concluídas com sucesso!")
else:
    print("A pasta 'origem' não foi encontrada.")

