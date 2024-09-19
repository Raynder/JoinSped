
result_lines = {}
erros = {
    '0150': 0,
    '0190': 0,
    '0200': 0,
    '0400': 0,
}

last_line = ''

removeDuplicatesItems = [
    {'code': '0150', 'column': 2},
    {'code': '0190', 'column': 2},
    {'code': '0200', 'column': 3, 'inverse': True},
    {'code': '400', 'column': 2},
]

def mount_key(item, line_to_columns):
    if(not item['column']):
        key = item['key']+"_".join(line_to_columns)
    else:
        key = item['key']+'_'+line_to_columns[item['column']]
    return key

def write_text(line):
    global data_arquivo
    try:
        with open('resultado.txt', "a",encoding="utf-8") as arquivo:
            arquivo.write(line)
    except:
        with open('resultado.txt', "a",encoding="latin-1") as arquivo:
            arquivo.write(line)
    arquivo.close()

def order_dict(dictionary):
    if isinstance(dictionary, dict):
        ordered_dict = {}
        for key in sorted(dictionary.keys()):
            ordered_dict[key] = order_dict(dictionary[key])
        return ordered_dict
    elif isinstance(dictionary, list):
        return [order_dict(item) for item in dictionary]
    else:
        return dictionary
    
def clean_file(file):
    with open('resultado.txt', "w",encoding="utf-8") as arquivo:
        arquivo.close()

def create_block(line):
    global result_lines
    if(not line[1] in result_lines):
        result_lines[line[1]] = {}
    return line[1]

def add_line(list, current_key, line_to_columns, subKey = None):
    if('childrenKey' in current_key):
        if(subKey in list[current_key['father']]):
            list[current_key['father']][subKey].append(('|').join(line_to_columns))
        elif(not subKey in list[current_key['father']]):
            list[current_key['father']][subKey] = [('|').join(line_to_columns)]
    else:
        if('unique' in current_key and current_key['key'] == line_to_columns[1] and subKey in list):
            return list
        elif('uniqueAll' in current_key and subKey in list and any(item.startswith("|".join(line_to_columns)[0:5]) for item in list[subKey])):
            return list
        elif(subKey in list):
            if('fatherKey' in current_key):
                if(not subKey in list):
                    list[subKey] = {}
                list[subKey][subKey].append(('|').join(line_to_columns))
            else:
                if('plus' in current_key):
                    field = ('|').join(line_to_columns)
                    if(any(item.startswith(field[0:10]) for item in list[subKey])):
                        field_current = next((item for item in list[subKey] if item.startswith(field[0:9])), None)
                        line = plus_fields(field, field_current, current_key['plus'])
                        list[subKey].remove(field_current)
                        list[subKey].append(line)
                    else:
                        list[subKey].append(('|').join(line_to_columns))
                elif('removeItemByColumn' in current_key and any(item_code['code'] == line_to_columns[1] for item_code in current_key['removeItemByColumn'])):
                    if(search_item(line_to_columns, current_key, list[subKey])):
                        return list
                    list[subKey].append(('|').join(line_to_columns))
                else:
                    list[subKey].append(('|').join(line_to_columns))
        elif(not subKey in list):
            if('fatherKey' in current_key):
                list[subKey] = {}
                list[subKey][subKey] = [('|').join(line_to_columns)]
            else:
                list[subKey] = [('|').join(line_to_columns)]
        
    return list

def order_dict(dictionary):
    if isinstance(dictionary, dict):
        ordered_dict = {}
        for key in sorted(dictionary.keys()):
            ordered_dict[key] = order_dict(dictionary[key])
        return ordered_dict
    elif isinstance(dictionary, list):
        return [order_dict(item) for item in dictionary]
    else:
        return dictionary

def search_item(line_to_columns, current_key, list):
    itemRemove = next((itemRemove for itemRemove in current_key['removeItemByColumn'] if itemRemove['code'] == line_to_columns[1]), None)
    search_item = "|".join(line_to_columns[0:itemRemove['column']+1])
    if('inverso' in itemRemove):
        search_item = "|".join(line_to_columns[-(len(line_to_columns)-itemRemove['column']):])
        if(any(item.endswith(search_item) for item in list)):
            erros[itemRemove['code']] = erros[itemRemove['code']] + 1
            return True

    if(any(item.startswith(search_item) for item in list)):
        erros[itemRemove['code']] = erros[itemRemove['code']] + 1
        return True
    False

def equival(line1, line2, regras):
    # Divide as linhas em partes usando o delimitador '|'
    partes_line1 = line1.split('|')
    partes_line2 = line2.split('|')
    if(partes_line1[1] not in regras):
        False
    
    # Itera sobre as regras
    for chave, colunas in regras.items():
        # Verifica se as linhas começam com a chave da regra
        if partes_line1[1] == chave and partes_line2[1] == chave:
            # Verifica se as colunas especificadas correspondem aos valores fornecidos nas regras
            for coluna in colunas:
                if partes_line1[coluna] != partes_line2[coluna]:
                    return False
            return True
    return False

def plus_fields(field1, field2, regras):
    # Divide as linhas em partes usando o delimitador '|'
    partes_field1 = field1.split('|')
    partes_field2 = field2.split('|')
    partes_new_field = field2.split('|')
    
    for chave, columns in regras.items():
        if partes_field1[1] == chave and partes_field2[1] == chave:
            for column in columns:
                if(',' in partes_field1[column] or ',' in partes_field2[column]):
                    value1 = float(partes_field1[column].replace(',','.'))
                    value2 = float(partes_field2[column].replace(',','.'))
                else:
                    value1 = int(partes_field1[column])
                    value2 = int(partes_field2[column])
                partes_new_field[column] = str(value1 + value2).replace('.',',')
    
    return "|".join(partes_new_field)

