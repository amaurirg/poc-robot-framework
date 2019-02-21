*** Settings ***
Documentation    Executando operações matemáticas
Library  ../scripts/sum.py


*** Test Cases ***
Soma
    [Tags]  soma
    Soma de Numeros     1   100

Subtracao
    [Tags]  subtracao
    Subtração de Numeros     100   99

Multiplicacao
    [Tags]  multiplicacao
    Multiplicação de Numeros     1   100

Divisao
    [Tags]  divisao
    Divisão de Numeros    100   10


