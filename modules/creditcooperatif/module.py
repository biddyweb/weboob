# -*- coding: utf-8 -*-

# Copyright(C) 2012 Kevin Pouget
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


from weboob.capabilities.base import find_object
from weboob.capabilities.bank import CapBank, AccountNotFound
from weboob.tools.backend import Module, BackendConfig
from weboob.tools.value import ValueBackendPassword, Value

from .perso.browser import CreditCooperatif as CreditCooperatifPerso
from .pro.browser import CreditCooperatif as CreditCooperatifPro


__all__ = ['CreditCooperatifModule']


class CreditCooperatifModule(Module, CapBank):
    NAME = 'creditcooperatif'
    MAINTAINER = u'Kevin Pouget'
    EMAIL = 'weboob@kevin.pouget.me'
    VERSION = '1.2'
    DESCRIPTION = u'Crédit Coopératif'
    LICENSE = 'AGPLv3+'
    auth_type = {'particular': "Interface Particuliers",
                 'weak' : "Code confidentiel (pro)",
                 'strong': "Sesame (pro)"}
    CONFIG = BackendConfig(Value('auth_type', label='Type de compte', choices=auth_type, default="particular"),
                           ValueBackendPassword('login', label='Code utilisateur', masked=False),
                           ValueBackendPassword('password', label='Code confidentiel ou code PIN'))

    def create_default_browser(self):
        if self.config['auth_type'].get() == 'particular':
            self.BROWSER = CreditCooperatifPerso
            return self.create_browser(self.config['login'].get(),
                                       self.config['password'].get())
        else:
            self.BROWSER = CreditCooperatifPro
            return self.create_browser(self.config['login'].get(),
                                       self.config['password'].get(),
                                       strong_auth=self.config['auth_type'].get() == "strong")

    def iter_accounts(self):
        return self.browser.get_accounts_list()

    def get_account(self, _id):
        return find_object(self.browser.get_accounts_list(), id=_id, error=AccountNotFound)

    def iter_history(self, account):
        return self.browser.get_history(account)

    def iter_coming(self, account):
        return self.browser.get_coming(account)
