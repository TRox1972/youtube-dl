# coding: utf-8
from __future__ import unicode_literals

import re
from collections import defaultdict
from .common import InfoExtractor

# getting error
    # /usr/local/opt/python3/bin/python3.5:
    # Error while finding spec for
    # 'youtube_dl.__main__' (<class 'ImportError'>:
    # cannot import name 'parse_iso8301'); 'youtube_dl'
    # is a package and cannot be directly executed
# when importing
#from ..utils import parse_iso8301, unified_strdate


class FlipagramIE(InfoExtractor):
    IE_NAME = 'Flipagram'
    _VALID_URL = r'https?://(?:www\.)?flipagram\.com/f/(?P<id>[^/?_]+)'
    _TESTS = []

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        self.report_extraction(video_id)
        content_data = self._parse_json(re.search(r'..@context.+', webpage).group(0), video_id)
        user_data = self._parse_json(re.search(r'window.reactH2O\s*=\s*({.+});', webpage).group(1), video_id)

        thumbnails = [{}, {}, {}]
        i = 0
        for cover in user_data.get('flipagram').get('covers'):
            thumbnails[i]['url'] = 'http:' + cover.get('url')
            thumbnails[i]['width'] = cover.get('width')
            thumbnails[i]['height'] = cover.get('height')
            i += 1

        comments = []
        i = 0
        for comment in user_data.get('comments').get(video_id).get('items'):
            comments.append(
                    {
                        'author': comment.get('user').get('name'),
                        'author_id': comment.get('user').get('username'),
                        'id': comment.get('id'),
                        'text': comment.get('comment')[0],
                        #'timestamp': convert_to_iso(parse_iso8301(comment[i].get('created'))),
                        'parent': 'root'
                    }
                )

        tags = []
        i = 1
        for tag in user_data.get('flipagram').get('story'):
            if type(tag) == type({}):
                try:
                    tags.append(tag.itervalues().next())
                except AttributeError:
                    # Python 3.x
                    tags.append(next(iter(tag.values())))

        audio_url = user_data.get('flipagram').get('music').get('track').get('previewUrl')

        formats = [
            {
                'url': audio_url,
                'ext': 'm4a',
                'format_note': '(audio only)',
            },
            {
                'url': content_data.get('contentUrl'),
                'ext': 'mp4',
                'width': user_data.get('flipagram').get('video').get('width'),
                'height': user_data.get('flipagram').get('video').get('height'),
            }
        ]

        return {
            'id': video_id,
            'title': content_data.get('name'),
            'formats': formats,
            'ext': 'mp4',
            'thumbnails': thumbnails,
            'description': content_data.get('description'),
            'uploader': user_data.get('flipagram').get('user').get('name'),
            'creator': user_data.get('flipagram').get('user').get('name'),
            #'timestamp': parse_iso8301(user_data.get('flipagram').get('iso8601Created')),
            #'upload_date': unified_strdate(user_data.get('flipagram').get('created')),
            'uploader_id': user_data.get('flipagram').get('user').get('username'),
            'uploader_url': 'https://flipagram.com' + user_data.get('flipagram').get('user').get('username'),
            'view_count': user_data.get('flipagram').get('counts').get('plays'),
            'repost_count': user_data.get('flipagram').get('counts').get('reflips'),
            'comment_count': user_data.get('flipagram').get('counts').get('comments'),
            'comments': comments,
            'tags': tags,
            'is_live': False,
            'track': user_data.get('flipagram').get('music').get('track').get('title'),
            'track_id': user_data.get('flipagram').get('music').get('track').get('id'),
            'artist': user_data.get('flipagram').get('music').get('track').get('artistName'),
            'album': user_data.get('flipagram').get('music').get('track').get('albumName'),
        }
