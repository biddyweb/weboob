# -*- coding: utf-8 -*-

# Copyright(C) 2010-2015 Julien Veyssier, Laurent Bachelier
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.


import random
import urllib
from urlparse import urlsplit

from weboob.deprecated.browser import Browser, BrowserHTTPNotFound

from .pages.index import IndexPage
from .pages.torrents import TorrentPage, TorrentsPage

__all__ = ['PiratebayBrowser']


class PiratebayBrowser(Browser):
    ENCODING = 'utf-8'
    DOMAINS = ['thepiratebay.se']

    def __init__(self, url, *args, **kwargs):
        url = url or 'https://%s/' % random.choice(self.DOMAINS)
        url_parsed = urlsplit(url)
        self.PROTOCOL = url_parsed.scheme
        self.DOMAIN = url_parsed.netloc
        self.PAGES = {
            '%s://%s/' % (self.PROTOCOL, self.DOMAIN): IndexPage,
            '%s://%s/search/.*/0/7/0' % (self.PROTOCOL, self.DOMAIN): TorrentsPage,
            '%s://%s/torrent/.*' % (self.PROTOCOL, self.DOMAIN): TorrentPage
        }
        Browser.__init__(self, *args, **kwargs)

    def iter_torrents(self, pattern):
        self.location('%s://%s/search/%s/0/7/0' % (self.PROTOCOL,
                                                   self.DOMAIN,
                                                   urllib.quote_plus(pattern.encode('utf-8'))))

        assert self.is_on_page(TorrentsPage)
        return self.page.iter_torrents()

    def get_torrent(self, _id):
        try:
            self.location('%s://%s/torrent/%s/' % (self.PROTOCOL,
                                                   self.DOMAIN,
                                                   _id))
        except BrowserHTTPNotFound:
            return
        if self.is_on_page(TorrentPage):
            return self.page.get_torrent(_id)
