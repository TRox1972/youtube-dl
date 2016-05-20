# coding: utf-8
from __future__ import unicode_literals

import re
from .common import InfoExtractor


class SpoilerTVIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?spoilertv\.com/[^/]+/[^/]+/(?P<id>[^/?\.]+).*'
    _TEST = {}

    def _real_extract(self, url):
        display_id = self._match_id(url)

        webpage = self._download_webpage(url, display_id)

        video_id = self._search_regex(r'<iframe[^>]*id="[^_>]+_(?P<id>\d{7})"', webpage, display_id, group='id')
        self.report_extraction(video_id)

        m3u8_url = 'http://hls.springboardplatform.com/storage/Spoilertv.com/conversion/{}_2.mp4.m3u8'.format(video_id)
        print(m3u8_url)
        formats = self._extract_m3u8_formats(m3u8_url, video_id, 'mp4')
        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'formats': formats,
            'ext': 'mp4',
        }
