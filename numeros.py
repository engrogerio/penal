

extenso = ['um', 'dois', 'três', 'quatro', 'cinco', 'seis', 
        'sete', 'oito', 'nove', 'dez', 'onze', 'doze', 'treze',
        'quatorze', 'quinze', 'dezesseis', 'desessete', 'dezoito',
        'dezenove', 'vinte', 'vinte e um', 'vinte e dois', 'vinte e três',
        'vinte e quatro', 'vinte e cinco', 'vinte e seis', 'vinte e sete',
        'vinte e oito', 'vinte e nove', 'trinta']
numbers = range(1, 31)

def get_extenso() -> dict:
    """
    Returns a dictionary with numbers in portuguese text. Ex:{1: 'Um'}
    """
    return dict(zip(numbers, extenso))




