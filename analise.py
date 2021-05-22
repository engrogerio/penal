import numeros
import spacy

def analysis(text: str):
    nlp = spacy.load("pt_core_news_sm")
    for doc in nlp.pipe(text): #, disable=["tok2vec", "tagger", "parser", "attribute_ruler", "lemmatizer"]):
        # Do something with the doc here
        print('Resultado=>', [(ent.text) for ent in doc.tag])
        # print('Resultado=>', [(ent.text, ent.label_) for ent in doc.ents])

def separate(text):
    nlp = spacy.load("pt_core_news_sm")
    tokens = nlp(text)
    for sent in tokens.sents:
        print(sent) #.string.strip())

def get_text(file_name):
    lines = []
    fractions = get_fraction_numbers()
    with open(file_name, 'r', encoding='utf-8') as text:
    # removing empty lines and spaces
        for line in text:
            if len(line.strip()) == 0:
                continue # if line is empty, don't bring.

            # replace numbers in text (extenso) by digits
            numbers = numeros.get_extenso()
            for k,v in numbers.items():
                line = line.replace(f' {v} ', f' {k} ') 
 
            # replace fraction number in text: um sexto => 1/6
            for k,v in fractions.items():
                line = line.replace(f'{v} ', f'/{k} ')

            lines.append(line.strip())

    return lines

def get_roman_numbers():
    roman_numbers = [f'{n} -' for n in numeros.roman_numbers()]
    return roman_numbers

def get_fraction_numbers():
    return numeros.get_fractions()

def parse(line):
    loop_paragraph = False
    roman_numbers = get_roman_numbers()

    line_result = ''
 
    if any(line.startswith(x) for x in roman_numbers): 
        line_result += '\n\nInciso ==>' + line
    else:
        loop_paragraph = False

    if 'Art.' in line:
        line_result += f'\n\nArtigo ==>' + line
    if 'pena' in line.lower():
        line_result += f'\n\nPena ==>' + line[line.lower().find('pena'):]

    if 'aumentada' in line.lower():
        line_result += f'\n\nAgravante ==>' + line[line.lower().find('aumentada'):]

    if 'aumentar' in line.lower():
        line_result += f'\n\nAgravante ==>' + line[line.lower().find('aumentar'):]

    if 'diminuída' in line.lower():
        line_result += f'\n\nAtenuante ==>' +  line[line.lower().find('diminuída'):]

    if 'reduzir' in line.lower():
        line_result += f'\n\nAtenuante ==>' + line[line.lower().find('reduzir'):]

    if any(x in line for x in ['§', 'Parágrafo']):
        line_result += f'\n\nParágrafo ==>' + line
        loop_paragraph = True

    if not line_result:
        line_result += f'\n\nCrime ==>' + line
    return line_result

text_lines = get_text('decreto.txt')

for n, line in enumerate(text_lines):
    print(n, ' - ', line)
    print(n, ' - ', parse(line))
    print('\n=================================================================\n')



test_json = {
    "name": "Código Penal", "version": "2020-01-13",
    "text": 
    {
        "article": 
        {
            "number": "121",
            "title": "Homicídio Simples",
            "base_sentence": 
            {
                "type": "prisão",
                "unit": "anos",
                "minimum": 6,
                "maximum": 20,
                "referenced":
                {
                    "type": "lei",
                    "number": "13.104",
                    "year": "2015"
                }
            },
            "rules": 
            {
                "when": "Se o agente comete o crime impelido por motivo de relevante valor social ou moral, ou sob o domínio de violenta emoção, logo em seguida a injusta provocação da vítima",
                "then": 
                {
                    "type": "atenuante",
                    "unit": "fracão",
                    "minimum": "1/6",
                    "maximum": "1/3"
                }
            }
        }        
    }
}
