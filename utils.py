from collections import defaultdict
from typing import DefaultDict
import numeros
import re

def get_text(file_name) -> list:
    lines = []
    fractions = get_fraction_numbers()
    with open(file_name, 'r', encoding='utf-8') as text:
    # removing empty lines and spaces
        for line in text:
            #if len(line.strip()) == 0:
            #    continue # if line is empty, don't bring.

            # replace numbers in text (extenso) by digits
            numbers = numeros.get_extenso()
            for k,v in numbers.items():
                line = line.replace(f'{k} ', f'{v} ') 
 
            # TODO: replace fraction number in text: um sexto => 1/6
            # for k,v in fractions.items():
                # line = line.replace(f'{v} ', f'/{k} ')

            # replace all – by -
            line = line.replace('–', '-')
            lines.append(line.strip())

    return lines

def get_roman_numbers():
    roman_numbers = [f'{n}' for n in numeros.roman_numbers()]
    return roman_numbers

def get_fraction_numbers():
    return numeros.get_fractions()

def get_numbers() -> dict:
    return numeros.get_extenso()

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
    t3 = text_lines[line_number+3]
    # check if they are related to the entity
    if t1.isupper():
        text_lines[line_number] = text_lines[line_number] + ' - ' + t1
        text_lines[line_number+1] = ''
        if t2.isupper() and not any(x in t2 for x in ['CAPÍTULO', 'SEÇÃO']):
            text_lines[line_number] = text_lines[line_number] + ' ' + t2
            text_lines[line_number+2] = ''
        if t3.isupper() and not any(x in t3 for x in ['CAPÍTULO', 'SEÇÃO']):
            text_lines[line_number] = text_lines[line_number] + ' ' + t3
            text_lines[line_number+3] = ''
            
    return text_lines
        
def tag(line):
    defined = False
    result = []
    
    # revogado
    if '(revogado' in line.lower():
        defined = True
        result.append('revogado')
    
    # vetado
    if '(vetado' in line.lower():
        defined = True
        result.append('vetado')
    
    # referencia
    if 'Lei nº ' in line:
        # defined = True
        result.append('referencia')
    # parte
    if 'PARTE' in line and not defined:
        defined = True
        result.append('parte')
    # titulo
    if any(line.startswith(f'TÍTULO {x}') for x in get_roman_numbers()) and not defined:
        defined = True
        result.append('titulo')
    # capitulo
    if any(line.startswith(f'CAPÍTULO {x}') for x in get_roman_numbers()) and not defined: 
        defined = True
        result.append('capitulo')
    # seção
    if any(line.startswith(f'SEÇÃO {x}') for x in get_roman_numbers()) and not defined: 
        defined = True
        result.append('secao')
    # artigo
    if 'Art. ' in line  and not defined:
        # defined = True #
        result.append('artigo')
    # paragrafo
    if any(x in line for x in ["Parágrafo único", "§ "]) and not defined:
        # defined = True
        result.append('paragrafo')
    # pena
    if any(x in line for x in ['Pena - ', 'Pena: ']) and not defined:
        defined = True
        result.append('pena')
        
    # diminuicao 
    if any(x in line.lower() for x in ['reduzida', 'reduzir', 'diminuída']) and 'pena' in line.lower() and not defined:
        defined = True
        result.append('diminuicao')
    
    # aumento 
    if any(x in line.lower() for x in ['aumentada', 'aumentar', 'aumentam', 'aumenta-se']) and 'pena' in line.lower() and not defined:
        defined = True
        result.append('aumento')
    
    # inciso
    if any(line.startswith(f'{x} - ') for x in get_roman_numbers()) and not defined: 
        defined = True
        result.append('inciso')
        
    # alinea
    if re.search('^[a-z]\) ', line) and not defined:
        defined = True
        result.append('alinea')
    
    # vazio
    if line == '':
        defined = True
        result.append('vazio')
    
    # tipo
    if not defined:
        if ' de pena' not in line and ' da pena' not in line:
            if not re.search('^\(.*\)', line):
                result.append('tipo')
            
    return result

def get_all_entitie_lines(text_lines, entity):
    """
    return all document line numbers for the entity passed as parameter.
    """
    lines = []
    for n, line in enumerate(text_lines):
        classification = tag(line)
        if all(x in classification for x in [entity]):
            lines.append(n)
    return lines

def apply_corrections(text_lines):
    # replace line 2 by line 1 and vice versa
    text_lines[0], text_lines[1] = text_lines[1], text_lines[0]
    
    # replace line 3892 by line 3894 and vice versa
    text_lines[3892], text_lines[3894] = text_lines[3894], text_lines[3892]
    
    # replace line 3919 by line 3920 and vice versa
    text_lines[3919], text_lines[3920] = text_lines[3920], text_lines[3919]

    #lines 2476 replace 2478 and vice versa
    text_lines[2476], text_lines[2478] = text_lines[2478], text_lines[2476]
    
    # replace typo 1o by 1º on line 1870
    text_lines[1869] = text_lines[1869].replace('1o', '1º')


    # replace typo : by - on line 3677
    text_lines[3677] = text_lines[3677].replace(':', ' -')

    # removing lines 3553 and 3554
    # line 3554 should be all caps
    text_lines[3552] = text_lines[3554].upper()
    text_lines[3553] = ''
    text_lines[3554] = ''
    

    # line 1261 missing dash
    text_lines[1261] = 'III - ' + text_lines[1261][4:]
    
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
        
    # break lines with 2 penas
    # 3502
    line = text_lines[3502].split(' e ')
    text_lines[3502] = ' '.join(line[0:2])
    text_lines[3503] = 'Pena - ' + ' '.join(line[2:])
    
    # 3460
    line = text_lines[3460].split(' e ')
    text_lines[3460] = ' '.join(line[0:2])
    text_lines[3461] = 'Pena - reclusão ' + ' '.join(line[2:])

    # 3452
    line = text_lines[3452].split(' e ')
    text_lines[3452] = ' '.join(line[0:2])
    text_lines[3453] = 'Pena - ' + ' '.join(line[2:])
    
    # 2947
    line = text_lines[2947].split(' ou ')
    text_lines[2947] = line[0]
    text_lines[2948] = 'Pena - ' + line[1]
    
    # 2469 - remover typo: " de 15 "
    text_lines[2469] = text_lines[2469].replace(' de 15 ', '')
    
    # remover valores de moeda
    # das linhas 1281, 1714, 1728,
    # 2031 e 3452
    
    
    def cut_forward(text, word):    
        word_pos = text.find(word)
        # print(text, word_pos)
        return text[: word_pos+6]
    
    text_lines[1281] = cut_forward(text_lines[1281], 'multa')
    text_lines[1714] = cut_forward(text_lines[1714], 'multa')
    text_lines[1728] = cut_forward(text_lines[1728], 'multa')
    text_lines[2031] = cut_forward(text_lines[2031], 'multa')
    text_lines[3453] = cut_forward(text_lines[3453], 'multa')+' se o documento é particular.'
    text_lines[2815] = cut_forward(text_lines[2815], 'multa')
    
    return text_lines
