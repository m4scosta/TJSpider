# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Questao(scrapy.Item):
    prova = scrapy.Field()
    enunciado = scrapy.Field()
    alternativas = scrapy.Field()
    resposta = scrapy.Field()
