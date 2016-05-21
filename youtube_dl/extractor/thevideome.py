# coding: utf-8
from __future__ import unicode_literals

import re
from .common import InfoExtractor

from ..utils import int_or_none


class TheVideoMeIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?thevideo\.me/(?P<id>[0-9a-z]+)'
    _TEST = {
        'url': 'http://thevideo.me/zo5jqio9my56',
        'md5': 'ef4a1fba05e47bd23d2f1f08602e4abe',
        'info_dict': {
            'id': 'zo5jqio9my56',
            'title': '',
            'ext': 'mp4',
            'thumbnail': '',
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        embed_page = self._download_webpage('https://thevideo.me/embed-%s.html'
            % video_id, video_id)

        formats = []
        for video_format in re.findall(
            r'label:\s*["\'](?P<label>[^"\']+)["\'],\s*file:\s*["\'](?P<file>[^"\']+)["\']',
            embed_page):
            formats.append({
                'url': video_format[1],
                'format_id': video_format[0],
            })

        duration = int_or_none(self._search_regex(r'\'duration:\'\s*\'(\d+)\'', webpage, video_id))

        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'formats': formats,
            'thumbnail': self._og_search_thumbnail(webpage),
            'duration': duration
        }
