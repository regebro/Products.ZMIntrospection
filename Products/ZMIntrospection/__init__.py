# (C) Copyright 2004-2006 Nuxeo SAS <http://nuxeo.com>
# Authors:
# Stefane Fermigier <sf@nuxeo.com>
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
# $Id: __init__.py 46486 2006-06-13 15:45:52Z fguillaume $

__refresh_module__ = 0

import cgi
from BTrees import OOBTree, OIBTree

def introspection(self):
    secman = getSecurityManager()
    if not secman.checkPermission("Manage properties", self.this()):
        raise Unauthorized("Permission denied")

    path = self.REQUEST.get('path', '')
    if not path:
        obj = self
    else:
        obj = self
        for id in path.split("/"):
            try:
                obj = getattr(obj, id)
            except AttributeError:
                obj = obj.get(id, {})

    res = []

    try:
        object_vars = vars(obj).items()
    except TypeError:
        object_vars = [(key, obj[key]) for key in obj]

    object_vars.sort()
    for attr_name, attr_value in object_vars:
        if not path:
            attr_path = attr_name
        else:
            attr_path = path + '/' + attr_name

        if isinstance(attr_value, (OOBTree.OOBTree, OIBTree.OIBTree)):
            new_value = {}
            for name in attr_value:
                new_value[name] = attr_value[name]
        else:
            new_value = attr_value
            try:
                attr_vars = vars(new_value)
            except:
                attr_path = ''

        res.append({
            'attr_path': attr_path,
            'attr_name': attr_name,
            'attr_type': u'%s' % type(attr_value),
            'attr_value': pprint.pformat(new_value, indent=2)
        })
    return res

# Monkey-patching. Yuck.
try:
    import pprint
    from Globals import HTMLFile
    from App.Management import Tabs
    from OFS.SimpleItem import Item
    from AccessControl import getSecurityManager, Unauthorized

    def filtered_manage_options(self, REQUEST=None):
        # Append an Introspection tab to an object's management tabs
        tabs = self._oldxxx_filtered_manage_options(REQUEST)
        secman = getSecurityManager()
        if len(tabs) \
          and secman.checkPermission("Manage properties", self.this()):
            tabs.append({'label': 'Introspection',
                         'action': 'manage_introspection'})
        return tabs

    Tabs._oldxxx_filtered_manage_options = Tabs.filtered_manage_options
    Tabs.filtered_manage_options = filtered_manage_options

    Item.manage_introspection = HTMLFile('zmi/manage_introspection', globals())
    Item.introspection = introspection

    import logging
    logging.getLogger('ZMIntrospection').info("Applied patch.")

except:
    import traceback
    traceback.print_exc()

