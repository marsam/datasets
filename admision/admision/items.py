# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class AdmisionItem(Item):
    codigo = Field()
    nombre = Field()
    eap = Field()
    puntaje = Field()
    merito_eap = Field()
    obs = Field()
