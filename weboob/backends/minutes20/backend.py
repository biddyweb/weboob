# -*- coding: utf-8 -*-

# Copyright(C) 2011  Julien Hebert
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
"backend for http://20minutes.fr"

from weboob.capabilities.messages import ICapMessages
from weboob.tools.capabilities.messages.GenericBackend import GenericNewspaperBackend
from .browser import Newspaper20minutesBrowser
from .tools import rssid

class Newspaper20minutesBackend(GenericNewspaperBackend, ICapMessages):
    "Newspaper20minutesBackend class"
    MAINTAINER = 'Julien Hebert'
    EMAIL = 'juke@free.fr'
    VERSION = '0.9.1'
    LICENSE = 'AGPLv3+'
    STORAGE = {'seen': {}}
    NAME = 'minutes20'
    DESCRIPTION = u'20minutes French news  website'
    BROWSER = Newspaper20minutesBrowser
    RSS_FEED = 'http://www.20minutes.fr/rss/20minutes.xml'
    RSSID = rssid

