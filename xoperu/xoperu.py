#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
http://www.perueduca.edu.pe/olpc/OLPC_Dist.html
"""

import json
from ast import literal_eval
from itertools import imap

import urllib3


REGIONES = ['TUMBES', 'PIURA', 'LAMBAYEQUE', 'CAJAMARCA', 'LA LIBERTAD',
            'ANCASH', 'LIMA PROVINCIA', 'CALLAO', 'LIMA METROPOLITANA',
            'HUANCAVELICA', 'ICA', 'AYACUCHO', 'AREQUIPA', 'MOQUEGUA',
            'TACNA', 'PUNO', 'APURIMAC', 'CUSCO', 'MADRE DE DIOS', 'JUNIN',
            'PASCO', 'UCAYALI', 'HUANUCO', 'SAN MARTIN', 'AMAZONAS', 'LORETO',
            ]


def dstarmap(function, iterable):
    """
    Similar a itertools.starmap but takes keyword arguments.
    dstarmap(function, [{'a':2, 'b':3}, {'a':4, 'b':6}, ...])
    """
    for kwargs in iterable:
        yield function(**kwargs)


class XOScrapper(object):
    url = 'http://www.perueduca.edu.pe/utilAjax/olpc.do'

    def __init__(self):
        self.http = urllib3.PoolManager()

    def get_tipos(self, **kwargs):
        r = self.http.request('GET', self.url, {'metodo': 'getTipos', 'region': kwargs['region']})
        return [dict(d, **{'region': kwargs['region']}) for d in literal_eval(r.data)]

    def get_nivel(self, **kwargs):
        r = self.http.request('GET', self.url, {'metodo': 'getNivel', 'region': kwargs['region'], 'tipo': kwargs['tipo']})
        return [dict(d, **{'region': kwargs['region'], 'tipo': kwargs['tipo']}) for d in literal_eval(r.data)]

    def get_ugel(self, **kwargs):
        r = self.http.request('GET', self.url, {'metodo': 'getUgel', 'region': kwargs['region'], 'tipo': kwargs['tipo'], 'nivel': kwargs['nivel']})
        return [dict(d, **{'region': kwargs['region'], 'tipo': kwargs['tipo'], 'nivel': kwargs['nivel']}) for d in literal_eval(r.data)]

    def get_instituciones(self, **kwargs):
        r = self.http.request('GET', self.url, {'metodo': 'getInstituciones', 'region': kwargs['region'], 'tipo': kwargs['tipo'], 'nivel': kwargs['nivel'], 'ugel': kwargs['ugel']})
        return [dict(d, **{'region': kwargs['region'], 'tipo': kwargs['tipo'], 'nivel': kwargs['nivel'], 'ugel': kwargs['ugel']}) for d in literal_eval(r.data)]

    def run(self):
        result = []
        for tipo in imap(lambda reg: self.get_tipos(region=reg), REGIONES):
            for nivel in dstarmap(self.get_nivel, tipo):
                for ugel in dstarmap(self.get_ugel, nivel):
                    for u in dstarmap(self.get_instituciones, ugel):
                        result += u
        with open('xoperu.json', 'w') as f:
            json.dump(result, f, indent=2)


if __name__ == '__main__':
    xo = XOScrapper()
    xo.run()
