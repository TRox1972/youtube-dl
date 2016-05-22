# coding: utf-8
from __future__ import unicode_literals

import re
from .common import InfoExtractor

from ..utils import (
    int_or_none,
    parse_filesize,
)

class SibnetIE(InfoExtractor):
    IE_NAME = 'Sibnet.ru'
    _VALID_URL = r'https?://video\.sibnet\.ru/video(?P<id>\d{7})-(?P<display_id>[^/]+)'
    _TEST = {
        'url': 'https://video.sibnet.ru/video2588891-Podborka_prikolov_za_rulem/',
        'info_dict': {
            'id': '2588891',
            'title': 'Видео Подборка приколов за рулем',
            'ext': 'mp4',
            'thumbnail': 'http://video.sibnet.ru/upload/cover/video_2588891_0.jpg',
            'duration': 361,
        },
        'params': {
            # m3u8 download
            'skip_download': True
        }
    }

    def _real_extract(self, url):
        mobj = re.match(self._VALID_URL, url)
        video_id, display_id = mobj.group('id', 'display_id')

        webpage = self._download_webpage(url, display_id)

        formats = self._extract_m3u8_formats(
            'https://video.sibnet.ru' + self._search_regex(
            r'\'file\'\s*:\s*\'(/v/[a-z0-9]{32}/\d{7}_?.m3u8)\'',
            webpage, display_id), display_id, ext='mp4')

        filesize_approx = int_or_none(parse_filesize(self._search_regex(
            r'<td[^>]*class=video_size[^>]*>([^>]+)</td>', webpage, display_id)))

        return {
            'id': video_id,
            'title': self._og_search_title(webpage),
            'formats': formats,
            'thumbnail': self._og_search_thumbnail(webpage),
            'filesize_approx': filesize_approx,
            'duration': int_or_none(self._og_search_property('duration', webpage))
        }
