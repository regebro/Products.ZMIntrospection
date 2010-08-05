# (C) Copyright 2003 Nuxeo SARL <http://nuxeo.com>
# Author: Stefane Fermigier <sf@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
# $Id: testTab.py 19427 2004-11-07 14:46:40Z sfermigier $

from Testing import ZopeTestCase
import unittest, re

ZopeTestCase.installProduct("ZMIntrospection")

class IntrospectionTabTestCase(ZopeTestCase.ZopeTestCase):
    def testTabExists(self):
        self.setPermissions(["Manage properties"])
        self.login('test_user_1_')
        d = {'label': 'Introspection', 'action': 'manage_introspection'}
        assert d in self.app.test_folder_1_.filtered_manage_options()

    def testTabValue(self):
        self.app.toto = 'titi'
        assert self.app.introspection()
        assert re.search("toto", self.app.introspection())
        assert re.search("titi", self.app.introspection())

        # Make sure the DTML works by providing dummy arguments.
        class Response:
            def setHeader(self, *args):
                pass
        assert self.app.manage_introspection(self.app,
            RESPONSE=Response(), BASEPATH1=[''], URL='', URL1='', n_=0, a_=0,
            management_page_charset='')

def test_suite():
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    suite.addTest(loader.loadTestsFromTestCase(IntrospectionTabTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())
