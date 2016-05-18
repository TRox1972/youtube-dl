# coding: utf-8
from __future__ import unicode_literals

import re
from .common import InfoExtractor


class MSNIE(InfoExtractor):
	IE_NAME = 'MSN'
	_VALID_URL = r'https?://(?:www\.)?msn\.com/.+/[a-z]{2}-(?P<id>[a-zA-Z]+)'
	_TESTS = [{
		'url': 'http://www.msn.com/en-ae/foodanddrink/joinourtable/criminal-minds-shemar-moore-shares-a-touching-goodbye-message/vp-BBqQYNE',
		'md5': '2265d315b6cf3cd74c7a50caa2bb2d9d',
		'info_dict': {
			'id': 'BBqQYNE',
			'title': 'Criminal Minds - Shemar Moore Shares A Touching Goodbye Message',
			'description': 'Following news of his departure from the show, the star of Criminal Minds shares a heartwarming message to his fans and "baby girls."',
			'duration': '1:44',
			'ext': 'mp4'
		}, {
			'url': 'http://www.msn.com/en-ae/news/offbeat/meet-the-nine-year-old-self-made-millionaire/ar-BBt6ZKf',
			'md5': '6e03b302daa3b73a1e410d6ad99f4b64',
			'info_dict': {
				'id': 'BBt6ZKf',
				'title': 'All That Bling: Self-Made Millionaire Child Builds Fashion &amp; Jewellery Empire',
				'description': 'SELF-MADE millionaire Isabella Barrett enjoys splashing the cash on designer shoes and expensive labels – despite being just nine-years-old. Isabella lives a life of luxury, being chauffeur driven to her favourite shopping haunts, dining on fresh lobster and attending parties with her socialite friends. But despite the high heels, heavy make-up and bulging shopping bags, Isabella is still in primary school. Isabella became a millionaire at just six-years-old after launching her own clothing and jewellery line. Isabella shot to fame after appearing on American TV show Toddlers and Tiaras. Now the the fashion-obsessed young socialite has over 1.6 million online followers and considers herself a successful businesswoman in her own right. Videographer / director: Jackson Eagan, Brian Henderson Producer: Nora Hakramaj, Nick Johnson Editor: Sonia Estal',
				'duration': '5:50',
				'ext': 'mp4'
			}
		}
	}]

	def extract_subtitles(self, url, video_id):
		return {
			'ext': 'vtt',
			'data': url
		}

	def _real_extract(self, url):
		video_id = self._match_id(url)

		webpage = self._download_webpage(url, video_id)

		self.report_extraction(video_id)
		raw_data = re.search(r'data-metadata\s*=\s*".+"', webpage).group(0).replace('&quot;', '"')
		raw_data = raw_data.replace('data-metadata="', '')[:-1]
		data = self._parse_json(raw_data, video_id)

		#subtitles = self.extract_subtitles(data.get('files')[0], video_id)

		formats = []
		for video_file in data.get('videoFiles'):
			if not '.ism' in video_file:
				formats.append(video_file['url'].replace('&amp;', '&'))

		return {
			'id': video_id,
			'url': formats[0],
			'title': data.get('title'),
			'description': data.get('description'),
			'thumbnail': data.get('headlineImage')['url'],
			'duration': int(data.get('durationSecs')),
			'ext': 'mp4',
		}
