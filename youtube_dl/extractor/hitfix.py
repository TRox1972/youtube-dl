# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class HitFixIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?hitfix\.com/[^/?]+/(?P<id>[a-z0-9_-]+)'
    _TEST = {}

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        #reg = self._search_regex(r'window.kWidget.embed\(({.*\n?.*"),', webpage, video_id, group=1) + '}'
        #print(type(reg))

        #kaltura_ids = self._parse_json(self._search_regex(r'window.kWidget.embed\(({.*\n?.*"),',
        #                                webpage, video_id, group=1) + '}', video_id)

        #kaltura_ids = self._parse_json(reg, video_id)

        kaltura_ids = self._parse_json('{"targetId":"kaltura_player_140188","wid":"_1151292","uiconf_id":24014792,"flashvars":flashvars,"cache_st":"140188","entry_id":"0_bs4e24dd"}'.replace(':flashvar', ':"flashvar"'), video_id)


        kaltura_ids = self._parse_json(self._search_rege(r'window.kWidget.embed\(({.*\n?.*"),',
            webpage, video_id, group=1).replace('flashvar', ':"flashvar"'), video_id)

        return self.url_result('kaltura:%s%s'.format(kaltura_ids['wid'].replace('_', ''), kaltura_ids['entry_id']))
