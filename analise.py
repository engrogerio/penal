from utils import *

def apply_metadata(text_lines: list[dict]):
    """
    return text_lines with a dictionary for the metadata below:
    {
        "revogado": True,
        "vetado": False,
        "parte": "",
        "titulo": "",
        "capitulo": "",
        "secao": "",
        "tema": "",
        "artigo": "",
        "paragrafo": "",
        "pena": "",
        "diminuicao": "",
        "aumento": "",
        "inciso": "",
        "referencia": ""
    }
    """
    lines = []
    vazio = revogado = vetado = parte = titulo = capitulo = secao = tema = artigo = paragrafo = alinea = pena = inciso = referencia = None
    capitulo_secao = titulo_capitulo = secao_artigo = capitulo_artigo = titulo_artigo = parte_artigo = None
    artigo_paragrafo = paragrafo_inciso = paragrafo_alinea = None
    metadata = {}
    for n, line in enumerate(text_lines):
        line_text = line.get('text', None)

        # revogado
        revogado = True if '(revogado' in line_text.lower() else False
        
        # vetado
        vetado = True if '(vetado' in line_text.lower() else False
          
        # referencia TODO: remove parentesis
        referencia_check = re.search('Lei nº [0-9]+.+', line_text)
        referencia = referencia_check.group() if referencia_check else referencia

        # parte
        parte_check = line_text.split(' ')[1] if 'PARTE' in line_text else None
        if parte_check:
            parte = parte_check 
            continue
        
        # titulo
        titulo_check = line_text if line_text.startswith('TÍTULO') else None
        if titulo_check:
            titulo = titulo_check  
            continue
                
        # capítulo
        # check if a capitulo is only inside its own titulo
        capitulo_check = line_text if line_text.startswith('CAPÍTULO') else None
        if capitulo_check:
            capitulo = capitulo_check
            titulo_capitulo = titulo
            continue
        else:
            if titulo_capitulo != titulo:
                capitulo = None  
            
            
        # seção
        # check if a seção is only inside its own capítulo
        secao_check = line_text if line_text.startswith('SEÇÃO') else None
        if secao_check:
            secao = secao_check
            capitulo_secao = capitulo
            continue
        else:
            if capitulo_secao != capitulo:
                secao = None    
        
        
        # artigo
        # check if an artigo is only inside its own capítulo or seção
        artigo_check = re.search('^Art\. [0-9]*-?.', line_text)
        if artigo_check:
            artigo = artigo_check.group()
            secao_artigo = secao
            capitulo_artigo = capitulo
            titulo_artigo = titulo
            parte_artigo = parte
            continue
        else:
            if secao_artigo != secao or capitulo_artigo != capitulo or titulo_artigo != titulo or parte_artigo != parte: 
                artigo = None    
        
        # paragrafo
        paragrafo_check = re.search('§ [0-9]+|Parágrafo único', line_text)
        if paragrafo_check:
            artigo_paragrafo = artigo
            paragrafo = paragrafo_check.group()
            continue
        else:
            if artigo_paragrafo != artigo:
                paragrafo = None
        
        # inciso should detect roman numerals
        # TODO match n spaces before roman numerals
        inciso_check = re.search('^ ?M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}) ', line_text)
        if inciso_check:
            paragrafo_inciso = paragrafo
            inciso = inciso_check.group()
            continue
        else:
            if paragrafo_inciso != paragrafo:
                inciso = None
        
        # pena
        # alinea
        alinea_check = re.search('^[a-z]\) ', line_text)
        if alinea_check:
            paragrafo_alinea = paragrafo
            alinea = alinea_check.group()
            continue
        else:
            if paragrafo_alinea != paragrafo:
                alinea = None
        
        # pena
        # pena = True if any(x in line_text for x in ['Pena - ', 'Pena: ']) else False
        # pena_check = line_text.startswith()('§ [0-9]+|Parágrafo único', line_text)
        # if paragrafo_check:
        #     paragrafo = paragrafo_check.group()
        #     continue
        
        # diminuicao 
        diminuicao = True if any(x in line_text.lower() for x in ['reduzida', 'reduzir', 'diminuída']) and 'pena' in line_text.lower() else False
        
        # aumento 
        aumento = True if any(x in line_text.lower() for x in ['aumentada', 'aumentar', 'aumentam', 'aumenta-se']) and 'pena' in line_text.lower() else False
        
       
        # vazio
        vazio = True if len(line_text) == 0 else False
        
        # tipo
        
        # if ' de pena' not in line and ' da pena' not in line and not re.search('^\(.*\)', line):
        #     result.append('tipo')
        
        metadata['vazio'] = vazio
        metadata['revogado'] = revogado
        metadata['vetado'] = vetado 
        metadata['parte'] = parte
        metadata['titulo'] = titulo
        metadata['capitulo']= capitulo
        metadata['secao'] = secao
        metadata['tema'] = tema
        metadata['artigo'] = artigo
        metadata['paragrafo'] = paragrafo
        metadata['pena'] = pena
        metadata['diminuicao'] = diminuicao
        metadata['aumento'] = aumento
        metadata['inciso'] = inciso
        metadata['alinea'] = alinea
        metadata['referencia'] = referencia 
        
        lines.append(dict(text=line, metadata=metadata.copy()))
        metadata = {}
    return lines

def get_tag_end_line(text_lines: list, start_line: int, tag: str) -> int:
    """
    Returns the line which has the same tag as the start.
    Ex. user requests an Article in line 2000. This method returns
    a line number where is the next Article starting from line 2000
    which is where the requested Article ends.
    
    :param tag: One of the tags: 
    # parte, titulo, capitulo, seção, artigo, paragrafo,
    # pena, atenuante, agravante, inciso, alinea, tipo
    """
    # get next tag line number with the same type 
    # ex. start = capitulo I , end = capitulo II
    lines = get_lines_by_tag(text_lines[start_line:], [tag,])
    # Lets grab the line before the next tag start (-1)
    end_line = lines[1][1][0] - 1
    return end_line

def get_penalties(line: str):
    
    """
    Retorna para cada linha, se existir, uma list de dict para cada pena:
    # <tipo>: "detenção", "reclusão", "e multa", "ou multa"
        "<tipo>":  
        {
            "unidade": unidade,
            "maximo": maximo,
            "minimo": minimo
        }
    
    """
    numbers = get_numbers()
    # numbers.update(duration_unit)
    line_content = line[1]
    key_names = {0: 'minimo', 1:'maximo'}
    durations = re.findall(r'dia .*?|dias.*?|mês.*?|meses.*?|ano.*?|anos.*?', 
                        line_content.lower())

    
    tipos = re.findall(r'detenção.*?|reclusão.*?|e multa.*?|ou multa.*?| multa.*?', 
                        line_content.lower())
    
        
    pena_int = [int(s) for s in line_content.split() if s.isdigit() and len(s)<3]

    # complete the duration when its specified just once.
    if len(durations) < len(pena_int):
        for _ in range(len(pena_int)-len(durations)):
            durations.append(durations[0])
    
    # separate text after the last pena duration
    posicao_multa = line_content.find('multa,')
    int_pos = posicao_multa + 6 if posicao_multa >0 else 0
    condicao_multa = None
    if int_pos>1:
        condicao_multa = line_content[int_pos:]
    
    # pena dict should be:
    """
    {
      "pena":
        [
          {
            "tipo": "reclusão",
            "duracao": 
              {
                "minimo": 
                  {
                    "valor": 2,
                    "unidade": "ano"
                  },
                "maximo":
                  {
                    "valor": 6,
                    "unidade": "ano"
                  }
              }
          },
          {
            "tipo": "e multa"
          },
          {
            "condicao": "no caso de dolo"  
          }       
        ]
    }
    """
    pena_dict = dict()
    if 'multa' not in tipos[0]:
        pena_dict = {
            "pena":
                [
                    {
                        "tipo": tipos[0],
                        "duracao": 
                        {
                            "minimo": 
                            {
                                "valor": pena_int[0],
                                "unidade": durations[0]
                            },
                            "maximo":
                            {
                                "valor": pena_int[1],
                                "unidade": durations[1]
                            }
                        }
                    }
                ]
        }
    # append if there is multa... 
     
    #       {
    #         "tipo": "e multa"
    #       },
    #       {
    #         "condicao": "no caso de dolo"  
    #       }       
    #     ]
    # }
    print(tipos, durations, pena_int, condicao_multa)
    
    # return data

def apply_penalties(text_lines) -> list:
    """
    Add penas data to the line if there is one:
    (law line number, law text, list of tags, penas)
    
    """
    lines = []
    for n, line in enumerate(text_lines):
        classification = line[2]
        pena=''
        if 'pena' in classification:
            pena = get_penalties(line)
        item = (line[0], line[1], line[2], pena)
        lines.append (item)
    return lines

def apply_tags(text_lines) -> list:
    """
    Returns a list of dictionaries with:
    (law line number, law text, list of tags)
    
    """
    lines = []
    for n, line in enumerate(text_lines):
        tags = tag(line)

        item = dict(line=n, text=line, tags=tags)
        lines.append (item)
    return lines

def get_lines_by_tag(text_lines, tags: list) -> list:
    """
    Returns a list of tuples with:
    (counter, law line number, law text, list of tags)
    based on the tags passed as parameter.
    """
    lines = []
    count = 0
    for n, line in enumerate(text_lines):
        classification = line[2]
        if any(x in classification for x in tags):
            count += 1
            item = (count, line)
            lines.append (item)
    return lines

# main ######
def main():
    text_lines = get_text('decreto.txt')
    text_lines = apply_corrections(text_lines)
    text_lines = apply_tags(text_lines)
    text_lines = apply_metadata(text_lines)
    # text_lines = a.apply_penalties(text_lines)
    # text_lines = a.apply_penalty_changes(text_lines)
    return text_lines

if __name__ == '__main__':
    lines = main()
    result = list()
    for line in lines:
        parte = line['metadata']['parte']
        titulo = line['metadata']['titulo'] 
        capitulo = line['metadata']['capitulo']
        secao = line['metadata']['secao']
        artigo = line['metadata']['artigo']
        paragrafo = line['metadata']['paragrafo']
        inciso = line['metadata']['inciso']
        alinea = line['metadata']['alinea']
        text = ((f'PARTE {parte}' or '-') + ' & ' 
                + (titulo or '-') + ' & ' 
                + (capitulo or '-') + ' & ' 
                + (secao or '-') + ' & ' 
                + (artigo or '-') + ' & '
                + (paragrafo or '-') + ' & '
                + (('INCISO ' if inciso else '') + (inciso or '-')) + ' & '
                + (('ALÍNEA ' if alinea else '') + (alinea or '-')) + ' & '
        )
        
        if text not in result:
            result.append(text)
    
    for line in sorted(result):     
        print(line, '\n')