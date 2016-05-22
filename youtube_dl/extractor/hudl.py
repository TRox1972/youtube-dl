# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor

from ..utils import (
    parse_duration,
    float_or_none,
)


class HudlIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?hudl\.com/[a-z0-9]+/\d{7}/[a-z0-9]+/(?P<id>\d{9})'
    _TEST = {
        'url': 'http://www.hudl.com/athlete/2538180/highlights/149298443',
        'md5': '16c3b7041b29d8ee35db0a20c2088f31',
        'info_dict': {
            'id': '149298443',
            'title': 'vs. Blue Orange Spring Game',
            'ext': 'mp4',
            'thumbnail': 'http://va.hudl.com/1dk/3tv/5c1123bb-0e22-433f-9060-12d377c3a1c5/7kdfv0nklnyqbkag-110_Hd720.jpg?v=1',
            'uploader': 'Nathaniel Snipes',
            'uploader_url': 'http://www.hudl.com/athlete/2538180',
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)

        embed_webpage = self._download_webpage(url.replace('hudl.com/', 'hudl.com/embed/', 1), video_id)

        data_info = self._parse_json(self._search_regex(
            r'window.__hudlEmbed\s*=\s*({.+}});',
            embed_webpage, video_id), video_id)['data']

        video_info = data_info['embeddablePlayer']['highlight']

        thumbnail = self._og_search_thumbnail(embed_webpage)

        return {
            'id': video_id,
            'title': video_info['title'],
            'url': video_info['videos']['sd'],
            'ext': 'mp4',
            'thumbnail': thumbnail if thumbnail else '',
            'uploader': video_info.get('ownerName'),
            'uploader_url': video_info.get('ownerPageUrl'),
            'duration': parse_duration(float_or_none(video_info.get('duration'))),
        }
