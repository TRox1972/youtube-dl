# coding: utf-8

import re
from .common import InfoExtractor


class MSNIE(InfoExtractor):
	IE_NAME = 'MSN' 
	_VALID_URL = r'https?://(?:www\.)?msn\.com/.+/vp-(?P<id>[a-zA-Z]+)'
	TESTS = []

	def extract_subtitles(self, url, video_id):
		sub_data = self._download_webpage(url, video_id)
		return {url: sub_data}

	def _real_extract(self, url):
		video_id = self._match_id(url)

		webpage = self._download_webpage(url, video_id)

		self.report_extraction(video_id)

		raw_data = re.search(r'data-metadata\s*=\s*".+"', webpage).group(0).replace('&quot;', '"')
		raw_data = raw_data.replace('data-metadata="', '')[:-1]
		data = self._parse_json(raw_data, video_id)

		formats = []
		for video_file in data.get('videoFiles'):
			#if 'blobrefkey' in video_file:
			if 1<2: # remove format 1001 (?)
				formats.append(video_file['url'].replace('&amp;', '&')]
		formats =  formats[1:] # need more elegant solution

		return {
			'id': video_id,
			'url': formats[1], # simple, but not correct. Remove and fix this
			'thumbnail': data.get('headlineImage')['url'],
			'title': data.get('title'),
			'description': data.get('description'),
			'ext': 'mp4',
			#'formats': formats[1:4],
		}
