import matplotlib.pyplot as plt
from wordcloud import WordCloud
import operator
from fpdf import FPDF
import glob, os

#var global de las palabras mas comunes de los papers
comunes = ["and","of", "the", "to", "is", "with", "a", "in", "or", "on", "for", "google"]

def separar_texto(pals):
    pals = pals.lower().replace('.',' ').replace(',', ' ').replace('#', ' ').replace('*',' ').replace(':',' ').replace('[',' ').replace(']',' ')
    return pals.split()

def generar_dict_filt(palabras_separadas, palabras_filtro, n):
    for i in palabras_filtro:
        try:
            while True:
                palabras_separadas.remove(i)
        except:
            pass

    contador = []
    for i in palabras_separadas:
        contador.append(palabras_separadas.count(i))

    #aca armo el diccionario
    my_dict = {}
    for i in range (len(palabras_separadas)):
        my_dict[palabras_separadas[i]] = contador[i]
    
    #ordeno el dic
    my_dict = dict(sorted(my_dict.items(), key=operator.itemgetter(1),reverse = True))

    #me quedo con las primeras n
    dict_n = {}
    cont = 0
    if n > 0:
        for i,j in my_dict.items():
            dict_n[i] = j
            cont += 1
            if cont == n:
                break
        return dict_n
    else:
        return my_dict   

def gen_wordcloud(texto):
    wordcloud = WordCloud(width=480, height=480, margin=0)
    wordcloud.generate_from_frequencies(texto)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)

def gen_clouds(namefile, todos):
    #abro mi archivo y separo el texto
    file = open(namefile)
    texto = file.read()
    file.close()
    if todos == False:
        texto = separar_texto(texto)
        #armo 1er diccionario
        texto_20 = generar_dict_filt(texto, comunes, 20)
        #para las 20 palabras
        gen_wordcloud(texto_20)
        plt.savefig('20pals{0}.png'.format(count))
    else:
        texto = separar_texto(texto)
        #armo 2do diccionario
        texto_todas = generar_dict_filt(texto, comunes, 0)
        #para todas las palabras
        gen_wordcloud(texto_todas)
        plt.savefig('todaspals.png')
        pdf = FPDF()
        pdf.add_page()
        pdf.image('todaspals.png')
        pdf.output("nube_final.pdf", "F")

#arranco a ejecutar mi programa
os.system("scrapy crawl messi")
print("Genero las nubes de los papers")
#var global para ponerle nombres a los pdfs
count = 1
all_files = []
#genero el pdf
pdf = FPDF()
for file in glob.glob("*.txt"):
    if (file != "contenedor.txt" and file != "todos_papers.txt") :
        #armo mi nube de 20 palabras para cada uno de los articulos
        print(file)
        gen_clouds(file, False)
        pdf.add_page()
        pdf.image('20pals{0}.png'.format(count))
        count += 1
pdf.output("clouds.pdf", "F")

print("Arranco haciendo mi archivo mayor")

for file in glob.glob("*.txt"):
    f = open("todos_papers.txt", 'a')
    arch = open(file)
    texto = arch.read()
    f.write(texto)
    arch.close()
f.close()
print("Ahora genero la nube de todos los articulos")
gen_clouds("todos_papers.txt", True)

#borro los archivos
os.remove("todos_papers.txt")
os.remove("todaspals.png")
for i in range(1,count):
    os.remove("20pals{0}.png".format(i))
os.remove("contenedor.txt")

print("listo :)")