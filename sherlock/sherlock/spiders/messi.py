import scrapy
import html2text
from datetime import datetime as dt

def extraer_links(texto):
    links = []
    i = 0
    while i < len(texto):
        index = texto.find("doi:") + 5
        #sumo 5 porque despues de la "d" de doi hay 5 caracteres
        if index != 4:
        #si el index es 4 significa que el find dio -1, es decir que no encontro la string que le mande
            j = 0
            while texto[index + j] != " ":
                #busco el primer espacio despues del doi, eso significa que termino
                j += 1
            links.append('https://dx.doi.org/'+ texto[index :j + index - 1])
            texto = texto [j + index:]
        i += 1
    return links

class MessiSpider(scrapy.Spider):
    name = 'messi'
    term = input("Input search term of interest: ")
    #size = input("# of papers to fetch (10, 20, 50, 100, 200): ")
    #allowed_domains = ['prueba.com']
    start_urls = ['https://pubmed.ncbi.nlm.nih.gov/?term={term}&filter=simsearch2.ffrft&size=20']

    def parse(self, response):
        converter=html2text.HTML2Text()
        converter.ignore_links=True
        converter.ignore_images=True
        converter.ignore_tables=True
        texto=converter.handle(response.css('*').get())
        #texto=texto.encode('ascii', 'ignore')
        f = open("contenedor.txt", 'w')
        f.write(texto)
        f.close()
        #escribo el archivo de links
        list_links = extraer_links(texto)
        for link in list_links:
            yield scrapy.Request(link, callback=self.parse_paper)
    
    def parse_paper(self, response):
        if hasattr(response, "text"):        
            converter=html2text.HTML2Text()
            converter.ignore_links=True
            converter.ignore_images=True
            converter.ignore_tables=True
            texto=converter.handle(response.css('*').get())
            #texto=texto.encode('ascii', 'ignore')
            f = open("{0}.txt".format(dt.now()), 'w')
            f.write(texto)
            f.close()
        