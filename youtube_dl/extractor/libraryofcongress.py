# coding: utf-8
from __future__ import unicode_literals

import re
from .common import InfoExtractor


class LibraryOfCongressIE(InfoExtractor):
    IE_NAME = 'LibraryOfCongress'
	_VALID_URL = r'https?://(?:www\.)?loc\.gov/item/(?P<id>[0-9]+)'
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
        'url': 'https://www.loc.gov/item/97516576/',
        'only_matching': True,
	}]

	def _real_extract(self, url):
		video_id = self._match_id(url)

		self.report_download_webpage(video_id)
		webpage = self._download_webpage(url, video_id)

		self.report_extraction(video_id)
		json_id = re.search('media-player-[0-9A-Z]{32}', webpage).group(0).replace('media-player-', '')
		data = self._parse_json(self._download_webpage('https://media.loc.gov/services/v1/media?id=%s' %json_id, video_id), video_id)
		data = data.get('mediaObject')

		media_url = data.get('derivatives')[0]['derivativeUrl']
		media_url = media_url.replace('rtmp', 'https')

		is_video = data.get('mediaType').lower() == 'v'
		if not (media_url.endswith('mp4') or media_url.endswith('mp3')):
			media_url += '.mp4' if is_video else '.mp3'

		if media_url.index('vod/mp4:') > -1:
			media_url = media_url.replace('vod/mp4:', 'hls-vod/media/') + '.m3u8'
		elif url.index('vod/mp3:') > -1:
			media_url = media_url.replace('vod/mp3:', '')

		if media_url.endswith('.m3u8'):
			formats = self._extract_m3u8_formats(media_url, video_id, ext='mp4')
		elif media_url.endswith('.mp3'):
			formats = media_url

		thumbnail_url = re.search(r'http://stream-media.loc.gov/ls/sagan/stills/[0-9]{7}-[0-9]-[0-9]_thumb.jpg',
			webpage).group(0)

		return {
			'id': video_id,
			'thumbnail': thumbnail_url,
			'title': self._og_search_title(webpage),
			'ext': 'mp4' if is_video else 'mp3',
			'formats': formats,
		}
