import re
from bs4 import BeautifulSoup
from datetime import datetime

def limpar_texto(texto):
    """ Remove quebras de linha e espaços extras do texto. """
    return ' '.join(texto.replace('\n', ' ').replace('\r', ' ').split())

def coletar_artigos(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    soup = BeautifulSoup(content, 'html.parser')
    ul_report = soup.find('ul', class_='report')
    artigos = []

    if ul_report:
        for li in ul_report.find_all('li', recursive=False):
            titulo = limpar_texto(li.find('h2').text)
            resumo_element = li.find('th', text='Resumo')
            resumo = limpar_texto(resumo_element.find_next('td').text) if resumo_element else "Resumo não encontrado"
            artigos.append({'Título': titulo, 'Resumo': resumo})
    
    return artigos

def encontrar_ocorrencias(artigos, termos_busca):
    for artigo in artigos:
        ocorrencias = []
        for termo in termos_busca:
            termo_regex = re.compile(termo, re.IGNORECASE)
            if termo_regex.search(artigo['Título']):
                ocorrencias.append(f'Título ({termo})')
            if termo_regex.search(artigo['Resumo']):
                ocorrencias.append(f'Resumo ({termo})')
        if ocorrencias:
            artigo['_SELECIONADO_'] = ', '.join(ocorrencias)

def salvar_resultados(artigos, somente_selecionados):
    agora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nome_arquivo = f"artigos_{agora}.txt"

    artigos_selecionados = [artigo for artigo in artigos if '_SELECIONADO_' in artigo]
    total_selecionados = len(artigos_selecionados)

    with open(nome_arquivo, 'w', encoding='utf-8') as file:
        for artigo in artigos:
            if somente_selecionados and '_SELECIONADO_' not in artigo:
                continue
            file.write(f'Título: {artigo["Título"]}\n')
            file.write(f'Resumo: {artigo["Resumo"]}\n')
            if '_SELECIONADO_' in artigo:
                file.write(f'MARCADO_PARA_LEITURA: {artigo["_SELECIONADO_"]}\n')
            file.write('\n')
        file.write(f'Total de artigos encontrados: {len(artigos)}\n')
        file.write(f'Total de artigos selecionados: {total_selecionados}\n')

    print(f'Resultados salvos em: {nome_arquivo}')

#file_path = 'base/r_completo1682-ACM.html'
#file_path = 'base/r_completo1178-SD.html'
file_path = 'base/r_completo1948-springer.html'
#file_path = 'base/r_completo43-IEEE.html'
#file_path = 'base/r_completo120-SCOPUS.html'
termos_busca = ['green', 'sustain', 'ecolog']
somente_selecionados = True

artigos = coletar_artigos(file_path)
encontrar_ocorrencias(artigos, termos_busca)
salvar_resultados(artigos, somente_selecionados)
