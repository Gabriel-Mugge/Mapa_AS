import csv
import textract
import os
import pandas as pd
import io

quests = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']

#varrendo o diretório para encontrar os pdfs referentes a lista
arquivos = [nome for nome in os.listdir()]
arquivos = [arq for arq in arquivos if os.path.isfile(arq)]
pdfs = [arq for arq in arquivos if arq.lower().endswith(".pdf")]

texto_to_split = list()
nomes = list()
for arq in pdfs:
    temp = arq.replace(".pdf", "")
    nomes.append(temp)
    texto = "2 - " + temp + "\\r\\n\\r\\nQuest~\\r\\nao"
    texto_to_split.append(texto)


#all_lists - lista de dicionarios contendo o nome do alunos e suas questões
#i - aluno atual
#questoes_lista questões da lista do aluno atual
#dicio_listas_cada_um - dicionario contendo nome e questões de cada aluno individual
all_lists = list()
for i in range(len(pdfs)):
    texto_lista = str(textract.process(pdfs[i]))
    questoes_lista = texto_lista.split(texto_to_split[i])
    del (questoes_lista[0])
    for j in range(len(questoes_lista) - 1):
        questoes_lista[j] = questoes_lista[j].replace("Lista", "")
        questoes_lista[j] = questoes_lista[j][2:]
        questoes_lista[j] = questoes_lista[j].rstrip(" ")
    questoes_lista[4] = questoes_lista[4][:-1]
    questoes_lista[4] = questoes_lista[4][2:]
    questoes_lista[4] = questoes_lista[4].rstrip(" ")
    dicio_listas_cada_um = {'nome': nomes[i], 'Q1': questoes_lista[0], 'Q2': questoes_lista[1], 'Q3': questoes_lista[2], 'Q4': questoes_lista[3], 'Q5': questoes_lista[4]}
    all_lists.append(dicio_listas_cada_um)


#i - refere-se ao aluno fixado para comparar com os demais, ou é a questão desse aluno fixada para
# comparar com as do outro.
# all_lists_math lista de dicionarios com os matchs
#num_quest_i - numero da questão analisada do aluno fixo
#num_quest_j - numero das questões dos outros alunos
#dicio_math_questoes - dicionario que salva os matchs do aluno i com os demais alunos
all_lists_math = list()
for i in range(len(pdfs)):
    math = ["", "", "", "", ""]
    for j in range(len(pdfs)):
        if i != j:
            for num_quest_i in range(len(quests)):
                for num_quest_j in range(len(quests)):
                    if all_lists[i][quests[num_quest_i]] == all_lists[j][quests[num_quest_j]]:
                        math[num_quest_i] += "[" + all_lists[j]['nome'] + "_" + str(num_quest_j + 1) + "]"

    dicio_math_questoes = {'nome': nomes[i], 'Q1': math[0], 'Q2': math[1], 'Q3': math[2], 'Q4': math[3], 'Q5': math[4]}
    all_lists_math.append(dicio_math_questoes)


#cria o csv
file = open("mapa.csv", 'w', encoding="utf8")
writer = csv.writer(file)
writer.writerow(('Aluno', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5'))


#salva os matchs dentro do csv
for i in range(len(pdfs)):
    writer.writerow((all_lists_math[i]['nome'], all_lists_math[i]['Q1'], all_lists_math[i]['Q2'], all_lists_math[i]['Q3'], all_lists_math[i]['Q4'], all_lists_math[i]['Q5']))

file.close()

#Abre o csv para leitura
dados_csv = pd.read_csv("mapa.csv")


#gera HTML
str_io = io.StringIO()
dados_csv.to_html(buf=str_io)
html_str = str_io.getvalue()
f = io.open("mapa.html", "w", encoding="utf-8")
f.write(html_str)
f.close()