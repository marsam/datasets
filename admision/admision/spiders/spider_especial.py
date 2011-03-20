
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from admision.items import AdmisionItem


def limpiar(lista):
  """devuelve un lista 'limpia' del feo \\xa0 """
  return map(lambda s: s.replace(u'\xa0', u''), lista)

class AdmisionEspecialSpider(CrawlSpider):
  name = 'especial' # solo especial 
  allowed_domains = ['200.14.241.13']
  start_urls = [
      'http://200.14.241.13/Website20110313especial/index.html',
      ]
  rules = (
      Rule(SgmlLinkExtractor(allow=('[A-Z]\.html'))),
      Rule(SgmlLinkExtractor(allow=('0\.html')), callback='parse_item', follow=True),
      Rule(SgmlLinkExtractor(allow=('[0-9]*\.html'), deny=('\.\./\.\./index\.html')), callback='parse_item'),
      )

  def parse_item(self, response):
    self.log('page: %s' % response.url)
    hxs = HtmlXPathSelector(response)
    codigos = limpiar(hxs.select('//tr/td[1]/text()').extract())
    nombres = hxs.select('//tr/td[2]/text()').extract()
    eap = hxs.select('//tr/td[3]/text()').extract()
    puntajes = limpiar(hxs.select('//tr/td[4]/text()').extract())
    merito_eap = limpiar(hxs.select('//tr/td[5]/text()').extract())
    obs = limpiar(hxs.select('//tr/td[6]/text()').extract())
    postulantes = zip(codigos, nombres, eap, puntajes, merito_eap, obs)
    items = []
    for postulante in postulantes:
      item = AdmisionItem()
      item['codigo'] = postulante[0]
      item['nombre'] = postulante[1]
      item['eap'] = postulante[2]
      item['puntaje'] = postulante[3]
      item['merito_eap'] = postulante[4]
      item['obs'] = postulante[5]
      items.append(item)
    return items

