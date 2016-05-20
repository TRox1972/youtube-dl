# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class CTVNewsIE(InfoExtractor):
    _VALID_URL = r'https://(?:www\.)ctvnews\.ca/video/.+'
    _TEST = {}

    def _real_extract(self, url):
        mobj = '' 
