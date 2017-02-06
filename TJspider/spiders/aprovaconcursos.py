# -*- coding: utf-8 -*-
import re
import scrapy
from string import printable
from TJspider.items import Questao


def clean_nonprintable(text):
    return ''.join(c for c in text if c in printable)


def gen_urls():
    base_url = 'https://www.aprovaconcursos.com.br/questoes-de-concurso/questoes/disciplina/Matem%25C3%25A1tica/banca/VUNESP/nivel/Ensino+M%25C3%25A9dio/filtro/2/pagina/{}'
    return (base_url.format(i) for i in range(1, 20))


class AprovaconcursosSpider(scrapy.Spider):
    name = "aprovaconcursos"
    allowed_domains = ["www.aprovaconcursos.com.br"]
    start_urls = gen_urls()

    def parse(self, response):
        yield self.parse_questoes(response)

    def parse_questoes(self, response):
        for q in response.css('.questao'):
            if self.tem_imagem(q):
                continue
            yield self.parse_questao(q)

    def parse_questao(self, q):
        questao = Questao()
        questao['prova'] = self.parse_prova(q)
        questao['enunciado'] = self.parse_enunciado(q)
        questao['alternativas'] = self.parse_alternativas(q)
        questao['resposta'] = self.parse_resposta(q)
        return questao

    def parse_prova(self, q):
        return q.css('.barra-top-2 span a::text')[0].extract()

    def parse_enunciado(self, q):
        selector = q.xpath('normalize-space(.//div[@class="enunciado row"])')
        return selector.extract()[0]

    def parse_alternativas(self, q):
        alternativas = {}
        for span in q.css('.alternativas .lbl span'):
            txt = span.xpath('normalize-space(.)')[0].extract()
            alternativas[txt[0]] = txt[2:].strip()
        return alternativas

    def parse_resposta(self, q):
        selector = '.alternativas input[data-correta="1"]::attr(data-opcao)'
        return q.css(selector)[0].extract().upper()

    def tem_imagem(selg, q):
        return q.css('.alternativas img') or q.css('.enunciado img')
