from utils import *
from datetime import datetime
import os

data_atual = datetime.now()
data_expiracao = datetime(2024, 5, 28)

if data_atual > data_expiracao:
    print('Licença expirada em:', data_expiracao.strftime('%d/%m/%Y'))
    exit()

def read_sped(nome, encode):
    with open(nome, 'r', encoding=encode) as origem:
        lines = origem.readlines()
        length_lines = len(lines)
        for i, line in enumerate(lines):
             # Calcular o percentual de progresso
            progresso_percentual = ((i + 1) / length_lines) * 100
            # Imprimir o progresso na saída do terminal
            print(f'Progresso: {progresso_percentual:.2f}%', end='\r')
            
            if(encode == 'latin-1'):
                line = line.encode('latin-1').decode('utf-8', 'ignore')
            line_to_columns = line.split('|')

            #Crie o bloco da linha caso ele não exista [0, A, C...]
            bloco = create_block(line)

            #Se a chave foi mapeada...
            if(line_to_columns[1] in keys):
                #Pega o objeto da chave correspondente
                current_range = keys[line_to_columns[1]]
                key = current_range['key']
                subKey = key

                #Para separar os pais com a mesma key, concatenamos com uma coluna
                if('column' in current_range):
                    key = mount_key(current_range, line_to_columns)
                #Se for um pai, guardamos seu nome para inerligar ao filho
                if('fatherKey' in current_range):
                    keyFather = key
                #Se for um filho, inerliga ao Pai que foi guardado o nome
                if('childrenKey' in current_range):
                    current_range['father'] = keyFather

            #Insira a linha com as propriedades correspondentes
            result_lines[bloco] = add_line(result_lines[bloco], current_range, line_to_columns, key)

clean_file('resultado.txt')

# Aqui colocamos as chaves que iniciam os arrays
# Colocamos algumas chaves para tratamentos especiais
# unique => linhas que são unicas
# uniqueAll => linhas unicas e seus proximos irmãos também são unicos
# column => indica a coluna que deve ser concatenada para gerar um index
# fatherKey => chaves que são filhos mas também são pais
# childrenKey => filhos das chaves que são fatherKey
# plus => linhas que tem algum tipo de soma, é passado a chave da linha e o array de colunas para somar
keys = {
    '0000': {'key': '0000', 'uniqueAll': True},
    '0140': {'key': '0140', 'column': 4,'unique': True},
    '0500': {'key': '0500', 'column': 7},
    '0500': {'key': '0600', 'column': 4},
    '0990': {'key': '0990', 'unique': True},
    
    'A001': {'key': 'A001', 'unique': True},
    'A010': {'key': 'A010', 'column': 2, 'fatherKey': True, 'unique': True},
    'A100': {'key': 'A100', 'childrenKey': True},
    'A990': {'key': 'A990', 'unique': True},

    'C001': {'key': 'C001', 'unique': True},
    'C010': {'key': 'C010', 'column': 2, 'fatherKey': True, 'unique': True},
    'C100': {'key': 'C100', 'childrenKey': True},
    'C180': {'key': 'C180', 'childrenKey': True},
    'C380': {'key': 'C380', 'childrenKey': True},
    'C400': {'key': 'C400', 'childrenKey': True},
    'C500': {'key': 'C500', 'childrenKey': True},
    'C600': {'key': 'C600', 'childrenKey': True},
    'C860': {'key': 'C860', 'childrenKey': True},
    'C990': {'key': 'C990', 'unique': True},

    'D001': {'key': 'D001', 'unique': True},
    'D010': {'key': 'D010', 'column': 2, 'fatherKey': True, 'unique': True},
    'D100': {'key': 'D100', 'childrenKey': True},
    'D200': {'key': 'D200', 'childrenKey': True},
    'D300': {'key': 'D300', 'childrenKey': True},
    'D500': {'key': 'D500', 'childrenKey': True},
    'D600': {'key': 'D600', 'childrenKey': True},
    'D990': {'key': 'D990', 'unique': True},

    'F001': {'key': 'F001', 'unique': True},
    'F010': {'key': 'F010', 'column': 2, 'fatherKey': True, 'unique': True},
    'F100': {'key': 'F100', 'childrenKey': True},
    'F200': {'key': 'F200', 'childrenKey': True},
    'F500': {'key': 'F500', 'childrenKey': True},
    'F600': {'key': 'F600', 'childrenKey': True},
    'F700': {'key': 'F700', 'childrenKey': True},
    'F800': {'key': 'F800', 'childrenKey': True},
    'F990': {'key': 'F990', 'unique': True},

    'I001': {'key': 'I001', 'unique': True},
    'I010': {'key': 'I010', 'column': 2, 'fatherKey': True, 'unique': True},
    'I100': {'key': 'I100', 'childrenKey': True},
    'I200': {'key': 'I200', 'childrenKey': True},
    'I300': {'key': 'I300', 'childrenKey': True},
    'I990': {'key': 'I990', 'unique': True},

    'M001': {'key': 'M001', 'unique': True},
    'M100': {'key': 'M100', 'column': 2},
    'M200': {'key': 'M200', 'unique': True},
    'M300': {'key': 'M300'},
    'M400': {'key': 'M400'},
    'M500': {'key': 'M500'},
    'M600': {'key': 'M600', 'unique': True},
    'M700': {'key': 'M700'},
    'M800': {'key': 'M800'},
    'M990': {'key': 'M990', 'unique': True},

    'P001': {'key': 'P001', 'unique': True},
    'P010': {'key': 'P010', 'column': 2, 'fatherKey': True, 'unique': True},
    'P100': {'key': 'P100', 'childrenKey': True},
    'P200': {'key': 'P200', 'childrenKey': True},
    'P990': {'key': 'P990', 'unique': True},

    '1001': {'key': '1001', 'unique': True},
    '1010': {'key': '1010'},
    '1990': {'key': '1990', 'unique': True},

    '9001': {'key': '9001', 'unique': True},
    '9900': {'key': '9900', 'plus': {'9900':[3]}},
    '9990': {'key': '9990', 'unique': True},
    '9999': {'key': '9999', 'unique': True}
}

# Aqui colocamos as chaves que não podem duplicar.
# Colocamos um array de colunas para ser analisado e comparados
duplicatesKeys = {
    '0150': [2,3],
    '0200': [2,3],
}

bloco = '0'
betweenKey = ''
keyFather = '0000'
data_arquivo = ''

arquivos = []
# Encontre os arquivos de origem e destino que estão na pasta que o app se encontra
for nome_arquivo in os.listdir(os.getcwd()):
    if nome_arquivo.startswith('origem') or nome_arquivo.startswith('destino'):
        data_arquivo = nome_arquivo[-10:-4]
        # Guarda o arquivo em um array
        arquivos.append({'nome': nome_arquivo, 'data': data_arquivo})

# Inicia a execução para cada arquivo de acordo com sua codificação
for arquivo in arquivos:
    print('Iniciando leitura do arquivo '+arquivo['nome']+'...')
    try:
        print('Leitura em UTF-8')
        read_sped(arquivo['nome'], 'utf-8')
    except Exception as e:
        print('Erro ao tentar ler em UTF-8\n\nIniciando leitura em Latin...')
        read_sped(arquivo['nome'], 'latin-1')

print('Iniciando escrita no arquivo de resultado...')
text_to_write = ''
last_line = ''
total_lines = 0
# Ordena todas as chaves e subchaves recursivamente
result_lines2 = order_dict(result_lines)
# Ultiliza o array desordenado para manter a orde original dos blocos
for bloco in result_lines:
    print('Escrevendo bloco ['+bloco+']...')
    total_block = 1
    length_block = len(result_lines[bloco])
    i = 0
    # Abre o bloco e começa a escrever suas linhas
    for key in result_lines2[bloco]:
        progresso_percentual = ((i + 1) / length_block) * 100
        # Imprimir o progresso na saída do terminal
        print(f'Progresso do bloco: {progresso_percentual:.2f}%', end='\r')
        # Contenha um fatherKey, a linha será tratada aqui
        if(not isinstance(result_lines2[bloco][key], list)):
            for item in result_lines2[bloco][key]:
                for line in result_lines2[bloco][key][item]:
                    if(line != last_line and not equival(line, last_line, duplicatesKeys)):
                        last_line = line
                        text_to_write = text_to_write+line
                        total_lines = total_lines + 1
                        total_block = total_block + 1
            write_text(text_to_write)
            text_to_write = ''
        # Caso seja uma linha normal, trataremos aqui
        else:
            lines = result_lines2[bloco][key]
            if(bloco == '1' or bloco == '0'):
                lines = sorted(lines)
            for line in lines:
                # Linhas de contadores usamos nossa contagem por bloco
                if(line[2:].startswith('990')):
                    if(line[1:].startswith('9990')):
                        text_to_write = '|9990|'+str(total_block + 1)+'|\n'
                    else:
                        text_to_write = '|'+key+'|'+str(total_block)+'|\n'
                    total_block = 1
                    total_lines = total_lines + 1
                    break
                elif(line[1:].startswith('9999')):
                    text_to_write = '|9999|'+str(total_lines + 1)+'|\n'
                # Para os blocos que contem mais de 2 listas, deixamos aberto por padrão |0|
                elif(key.endswith('001') and len(result_lines[bloco]) > 2):
                    if(line != last_line and not equival(line, last_line, duplicatesKeys)):
                        last_line = '|'+key+'|0|\n'
                        text_to_write = text_to_write+'|'+key+'|0|\n'
                        total_lines = total_lines + 1
                        total_block = total_block + 1
                # Tratativa normal para listas normais
                else:
                    if(line != last_line and not equival(line, last_line, duplicatesKeys)):
                        last_line = line
                        text_to_write = text_to_write+line
                        total_lines = total_lines + 1
                        total_block = total_block + 1
            # Escrevemos tudo o que foi concatenado e limpamos a variavel para iniciar a próxima lista
            write_text(text_to_write)
            text_to_write = ''
        i = i + 1

print('Processo finalizado!!!')
# Alteramos o nome do output pegando a data dos arquivos de input que contem antes do .txt
if(os.path.exists(os.getcwd()+'/resultado_'+data_arquivo+'.txt')):
    os.remove(os.getcwd()+'/resultado_'+data_arquivo+'.txt')
os.rename(os.getcwd()+'/resultado.txt', os.getcwd()+'/resultado_'+data_arquivo+'.txt')