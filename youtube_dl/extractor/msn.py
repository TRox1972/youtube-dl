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

		#self.report_download_webpage(video_id)
		webpage = self._download_webpage(url, video_id)

		self.report_extraction(video_id)

		raw_data = re.search(r'data-metadata\s*=\s*".+"', webpage).group(0).replace('&quot;', '"')
		raw_data = raw_data.replace('data-metadata="', '')[:-1]
		data = self._parse_json(raw_data, video_id)

		#_available_formats = []
		#[for formatCode in data.get('videoFiles') _available_formats.append(int(formatCode)]

		_available_formats = ['101', '102', '103', '104']

		_video_extensions = {
			'101': 'mp4',
			'102': 'mp4',
			'103': 'mp4',
			'104': 'mp4'
		}

		_video_dimensions = {
			'101': (320, 180),
			'102': (640, 360),
			'103': (640, 360),
			'104': (640, 360),
		} # difference between 102, 103 and 104?


		# TODO: Fix subtitles
		# ( http://prod.video.msn.com/tenant/amp/entityid/BBqQYNE?blobrefkey=en-us&$blob=1 )
		# ( http://prod.video.msn.com/tenant/amp/entityid/%s?blobrefkey=%s&$blob=1 % ( video_id, lang ) )


		formats = []
		#[for videoFile in data.get('videoFiles') formats.append(videoFile('url').replace('&amp;', '&'))]

		for video_file in data.get('videoFiles'):
			#if 'blobrefkey' in video_file:
			if 1<2:
				formats.append(video_file['url'].replace('&amp;', '&'))

		#for f in formats:
		#	print(f)
		#quit()

		#print(formats[1])


		return {
			'id': video_id,
			'url': formats[1], # simple, but not correct. Remove and fix this
			'thumbnail': data.get('headlineImage')['url'],
			'title': data.get('title'),
			'description': data.get('description'),
			'ext': 'mp4',
			#'formats': formats[1:4],

		}
