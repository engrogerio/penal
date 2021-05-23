import numeros
import re

def get_text(file_name) -> list:
    lines = []
    fractions = get_fraction_numbers()
    with open(file_name, 'r', encoding='utf-8') as text:
    # removing empty lines and spaces
        for n, line in enumerate(text):
            #if len(line.strip()) == 0:
            #    continue # if line is empty, don't bring.

            # replace numbers in text (extenso) by digits
            numbers = numeros.get_extenso()
            for k,v in numbers.items():
                line = line.replace(f' {v} ', f' {k} ') 
 
            # TODO: replace fraction number in text: um sexto => 1/6
            # for k,v in fractions.items():
                # line = line.replace(f'{v} ', f'/{k} ')

            lines.append(line.strip())

    
    
    return lines

def get_roman_numbers():
    roman_numbers = [f'{n}' for n in numeros.roman_numbers()]
    return roman_numbers

def get_fraction_numbers():
    return numeros.get_fractions()

def fix_broken_lines(text_lines, line_number):
    """
    Fix lines like: 
    CAPITULO I
    DAS ESPÉCIES DE PENA 
    
    to 
    CAPITULO I - DAS ESPÉCIES DE PENA 
    
    Método deve saber quantas linhas precisam ser agregadas.
    
    :param: line_number
    """
    t1 = text_lines[line_number+1]
    t2 = text_lines[line_number+2]
    # check if they are related to the entity
    if t1.isupper():
        text_lines[line_number] = text_lines[line_number] + ' - ' + t1
        text_lines[line_number+1] = ''
        if t2.isupper():
            text_lines[line_number] = text_lines[line_number] + t2
            text_lines[line_number+2] = ''
            
    return text_lines
        
def classify(line):
    defined = False
    result = []
    # referencia
    if 'Lei nº ' in line:
        defined = True
        result.append('referencia')
    # parte
    if 'PARTE' in line:
        defined = True
        result.append('parte')
    # titulo
    if any(line.startswith(f'TÍTULO {x}') for x in get_roman_numbers()):
        defined = True
        result.append('titulo')
    # capitulo
    if any(line.startswith(f'CAPÍTULO {x}') for x in get_roman_numbers()): 
        defined = True
        result.append('capitulo')
    # seção
    if any(line.startswith(f'SEÇÃO {x}') for x in get_roman_numbers()): 
        defined = True
        result.append('secao')
    # artigo
    if 'Art. ' in line:
        defined = True
        result.append('artigo')
    # paragrafo
    if any(x in line for x in ["Parágrafo único", "§ "]):
        defined = True
        result.append('paragrafo')
    # pena
    if 'Pena - ' in line:
        defined = True
        result.append('pena')
        
    # atenuante 
    if any(x in line.lower() for x in ['reduzida', 'reduzir', 'diminuída']) and 'pena' in line.lower():
        defined = True
        result.append('atenuante')
    
    # agravante 
    if any(x in line.lower() for x in ['aumentada', 'aumentar', 'aumentam']) and 'pena' in line.lower():
        defined = True
        result.append('agravante')
    
    # inciso
    if any(line.startswith(f'{x} - ') for x in get_roman_numbers()): 
        defined = True
        result.append('inciso')
    # alinea
    if re.search('^[a-z]\) ', line):
        defined = True
        result.append('alinea')
    # tema
    if not defined:
        result.append('tema')
    return result

def get_all_entitie_lines(text_lines, entity):
    """
    return all document line numbers for the entity passed as parameter.
    """
    lines = []
    for n, line in enumerate(text_lines):
        classification = classify(line)
        if line !='' and all(x in classification for x in [entity]):
            lines.append(n)
    return lines

def apply_corrections(text_lines):
    # replace line 2 by line 1 and vice versa
    text_lines[0], text_lines[1] = text_lines[1], text_lines[0]
    
    # replace typo 1o by 1º on line 1870
    text_lines[1869] = text_lines[1869].replace('1o', '1º')

    # removing lines 3553 and 3554
    text_lines[3552] = ''
    text_lines[3553] = ''
    
    # fix broken CAPÍTULO lines
    line_numbers = get_all_entitie_lines(text_lines, 'capitulo')
    for line_number in line_numbers:
        fix_broken_lines(text_lines, line_number)
        
    # fix broken SEÇÃO lines
    line_numbers = get_all_entitie_lines(text_lines, 'secao')
    for line_number in line_numbers:
        fix_broken_lines(text_lines, line_number)

    # fix broken TÍTULO lines
    line_numbers = get_all_entitie_lines(text_lines, 'titulo')
    for line_number in line_numbers:
        fix_broken_lines(text_lines, line_number)
    
    return text_lines

def referencias(line):
    lines = {}
    for n, line in enumerate(text_lines):
        if 'Lei nº ' in line:
            lines[line] = {}
            lines[line]["line_number"] = n
            lines[line]["lei"] = text_lines[n]
    return lines
          
def partes(text_lines):
    lines = {}
    for n, line in enumerate(text_lines):
        if 'PARTE' in line: 
            lines[line] = {}
            lines[line]["line_number"] = n
            lines[line]["name"] = text_lines[n]

    return lines

def titulos(text_lines):
    lines = {}
    roman_numbers = get_roman_numbers()
    for n, line in enumerate(text_lines):
        if any(line.startswith(f'TÍTULO {x}') for x in roman_numbers): 
            lines[line] = {}
            lines[line]["line_number"] = n
            lines[line]["name"] = text_lines[n+1]
    return lines

def capitulos(text_lines):
    lines = {}
    roman_numbers = get_roman_numbers()
    for n, line in enumerate(text_lines):
        if any(line.startswith(f'CAPÍTULO {x}') for x in roman_numbers): 
            lines[line] = {}
            lines[line]["line_number"] = n
            lines[line]["name"] = text_lines[n+1]
    return lines

text_lines = get_text('decreto.txt')
text_lines = apply_corrections(text_lines)

lines = []
count = 0
for n, line in enumerate(text_lines):
    classification = classify(line)
    if line != '' and all(x in classification for x in ['secao']):
        count += 1
        print((n, line, classification))
        print('==================================================')
print(f'{count} ocorrências')
