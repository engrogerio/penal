import numeros


with open('decreto.txt', 'r', encoding='utf-8') as decreto:
    lines = []
    loop_paragraph = False
    roman_numbers = ['I -', 'II -', 'III -', 'IV -', 'V -', 'VI -', 'VII -', 'VIII -', 'IX -', 'X -']
    numbers = numeros.get_extenso()

    # removing empty lines and spaces
    for line in decreto:
        if len(line.strip()) == 0:
            continue # if line is empty, don't bring.

        # replace numbers in text (extenso) by digits
        for k,v in numbers.items():
            search = f' {v} ' 
            if search in line:
                line = line.replace(v, str(k)) 
       
        lines.append(line.strip())

    for line in lines:
        # if loop_paragraph:
            
        if any(line.startswith(x) for x in roman_numbers): 
            print('Inciso ==>', line)
        else:
            loop_paragraph = False

        if 'Art.' in line:
            print('Artigo ==>', line)
        if 'pena' in line.lower():
            print('Pena ==>', line[line.lower().find('pena'):])

        if 'aumentada' in line.lower():
            print('Agravante ==>', line[line.lower().find('aumentada'):])
 
        if 'aumentar' in line.lower():
            print('Agravante ==>', line[line.lower().find('aumentar'):])

        if 'diminuída' in line.lower():
            print('Atenuante ==>', line[line.lower().find('diminuída'):])
 
        if 'reduzir' in line.lower():
            print('Atenuante ==>', line[line.lower().find('reduzir'):])

        if any(x in line for x in ['§', 'Parágrafo']):
            print('Parágrafo ==>', line)
            loop_paragraph = True

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
