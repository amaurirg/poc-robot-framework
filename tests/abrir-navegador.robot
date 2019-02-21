*** Settings ***
Documentation    Abrindo o navegador
Library  SeleniumLibrary
Library  ../scripts/SeleniumLibraryTeste.py

*** Variables ***
${DELAY}    1


*** Test Cases ***
Cenario1: Abrir o navegador do jeito padrão
    [Tags]  navegador-google
    Abrir o Chrome na pagina <http://www.google.com.br> do jeito padrão
    Colocar um delay do jeito padrão
    Fechar o browser do jeito padrão


Cenario2: Abrir o navegador do nosso jeito
    [Tags]  navegador-onecloud
    Abrir o Chrome na pagina <https://app.onecloudportal.com.br/#/login> do nosso jeito
    Colocar um delay do nosso jeito
    Fechar o browser do nosso jeito



*** Keywords ***
# Keywords utilizando o codigo padrão do Selenium
Abrir o ${browser} na pagina <${url}> do jeito padrão
    SeleniumLibrary.Open Browser  ${url}  ${browser}

Colocar um delay do jeito padrão
    SeleniumLibrary.Set Selenium Speed  ${DELAY}

Fechar o browser do jeito padrão
    Sleep    5s
    SeleniumLibrary.Close Browser



# Keywords utilizando o nosso codigo
Abrir o ${browser} na pagina <${url}> do nosso jeito
    SeleniumLibraryTeste.Open Navegador     ${url}  ${browser}

Colocar um delay do nosso jeito
    SeleniumLibraryTeste.Set Selenium Speed  ${DELAY}

Fechar o browser do nosso jeito
    Sleep    5s
    SeleniumLibraryTeste.Close Browser


