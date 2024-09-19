import os
import shutil
import subprocess

# Caminho para o diretório atual onde seu aplicativo está sendo executado
diretorio_atual = os.getcwd()

# Caminho para a pasta "origem"
pasta_origem = os.path.join(diretorio_atual, 'arquivos_divididos')

# Verifica se a pasta "origem" existe
if os.path.exists(pasta_origem) and os.path.isdir(pasta_origem):
    # Lista todas as pastas dentro da pasta "origem"
    subpastas = [subpasta for subpasta in os.listdir(pasta_origem) if os.path.isdir(os.path.join(pasta_origem, subpasta))]
    
    # Caminho para o arquivo "bot.exe"
    caminho_bot_exe = os.path.join(diretorio_atual, 'joinspedbot.exe')

    # Para cada subpasta, copia o arquivo "bot.exe" e executa-o
    for subpasta in subpastas:
        # Caminho para a subpasta
        caminho_subpasta = os.path.join(pasta_origem, subpasta)

        # Copia o arquivo "bot.exe" para a subpasta
        shutil.copy(caminho_bot_exe, caminho_subpasta)

        # Caminho para o "bot.exe" dentro da subpasta
        caminho_bot_exe_subpasta = os.path.join(caminho_subpasta, 'joinspedbot.exe')

        os.chdir(caminho_subpasta)

        # Executa o "bot.exe" dentro da subpasta
        subprocess.run(caminho_bot_exe_subpasta, shell=True)
        for arquivo in os.listdir(caminho_subpasta):
            if arquivo.startswith('resultado'):
                shutil.copy(caminho_subpasta+'/'+arquivo, diretorio_atual)
                break

    print("Arquivo 'joinspedbot.exe' copiado e executado em todas as subpastas dentro de 'arquivos'.")
else:
    print("A pasta 'arquivos' não foi encontrada ou não é um diretório.")
