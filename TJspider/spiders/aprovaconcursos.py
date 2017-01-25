# -*- coding: utf-8 -*-
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
        raw_enunciado = q.css('.enunciado *::text').extract()
        return ''.join(map(lambda t: t.strip(), raw_enunciado))

    def parse_alternativas(self, q):
        raw_texts = q.css('.alternativas .lbl *::text').extract()
        text = ''.join(map(lambda t: t.strip(), raw_texts))
        texts = text.strip('.').split('.')
        return dict(map(lambda t: (t[0], t[2:]), texts))

    def parse_resposta(self, q):
        selector = '.alternativas input[data-correta="1"]::attr(data-opcao)'
        return q.css(selector)[0].extract().upper()

    def tem_imagem(selg, q):
        return q.css('.alternativas img')
