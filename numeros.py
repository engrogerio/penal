def get_fractions():
    fractions = ['um', 'metade', 'terço', 'quarto', 'quinto', 'sexto']
    numbers = [1, 1/2, 1/3, 1/4, 1/5, 1/6]
    result = dict(zip(fractions, numbers))
    result['dobro'] = 2
    
def get_extenso() -> dict:
    """
    Returns a dictionary with numbers in portuguese text. Ex:{1: 'Um'}
    """
 
    extenso = ['um', 'dois', 'três', 'quatro', 'cinco', 'seis', 
        'sete', 'oito', 'nove', 'dez', 'onze', 'doze', 'treze',
        'quatorze', 'quinze', 'dezesseis', 'desessete', 'dezoito',
        'dezenove', 'vinte', 'vinte e um', 'vinte e dois', 'vinte e três',
        'vinte e quatro', 'vinte e cinco', 'vinte e seis', 'vinte e sete',
        'vinte e oito', 'vinte e nove', 'trinta']
    numbers = range(1, 31)

    return dict(zip(extenso, numbers))

def roman_numbers():

    roman_numbers = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
    return roman_numbers



