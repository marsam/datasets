
SPIDERS=secundaria primeros_puestos heroes_victimas comunidades_nativas discapacitados general especial total
FORMAT=csv

crawl:
	for SPIDER in $(SPIDERS); do	\
		echo crawling for $${SPIDER} spider;	\
		scrapy crawl $${SPIDER} --set FEED_URI=file://$(shell pwd)/postulantes_$${SPIDER}.$(FORMAT) --set FEED_FORMAT=$(FORMAT) ;\
	done	 		

clean:
	rm -f *.$(FORMAT)
	find . -iname '*.pyc' -exec rm -f {} \;


