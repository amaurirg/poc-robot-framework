from SeleniumLibrary.base import keyword


@keyword('Soma de Numeros', tags=['numeros'])
def addition(n1=0, n2=100):
    n1 = int(n1)
    n2 = int(n2)
    assert ((n1+n2) >= 100)


@keyword('Subtração de Numeros', tags=['numeros'])
def subtraction(n1, n2):
    n1 = int(n1)
    n2 = int(n2)
    assert ((n1-n2) >= 0)


@keyword('Multiplicação de Numeros', tags=['numeros'])
def multiplication(n1, n2):
    n1 = int(n1)
    n2 = int(n2)
    assert ((n1*n2) == 10)


@keyword('Divisão de Numeros', tags=['numeros'])
def division(n1, n2):
    n1 = int(n1)
    n2 = int(n2)
    assert ((n1/n2) >= 0)
