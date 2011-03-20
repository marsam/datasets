# Scrapy settings for admision project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'admision'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['admision.spiders']
NEWSPIDER_MODULE = 'admision.spiders'
DEFAULT_ITEM_CLASS = 'admision.items.AdmisionItem'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

