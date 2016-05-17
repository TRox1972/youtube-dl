# coding: utf-8

from __future__ import unicode_literals

import re

from .common import InfoExtractor

class LibraryOfCongressIE(InfoExtractor):
    IE_NAME = 'LibraryOfCongress'
    _VALID_URL = r'https?://www.loc.gov/item/(?P<id>[0-9]+)'

    _TESTS = [{
        'url': 'http://loc.gov/item/90716351/',
        'info_dict': {
            'id': '90716351',
            'ext': 'mp4',
            'title': 'Pa\'s trip to Mars /'
        },
        'params': {
            # m3u8 download
            'skip_download': True,
        }
    }, {
        'url': 'https://www.loc.gov/item/97516576/'
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        self.report_extraction(video_id)
        
        m3u8_id = re.search(r'media_service [0-9]{7}-[0-9]-[0-9]', webpage).group()[14:]
        m3u8_url = 'http://stream-media.loc.gov/hls-vod/media/ls/sagan/%s.mp4.m3u8' % m3u8_id

        formats = self._extract_m3u8_formats(m3u8_url, video_id, ext='mp4')

        return {
            'id': video_id,
            'thumbnail': 'http://stream-media.loc.gov/ls/sagan/stills/%s_thumb.jpg' % m3u8_id,
            'title': self._og_search_title(webpage),
            'ext': 'mp4',
            'formats': formats,
        }
