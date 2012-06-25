# -*- coding:utf-8 -*-

import Globals
from five import grok

from Products.CMFQuickInstallerTool.interfaces import INonInstallable \
    as INonInstallableProducts
from Products.CMFPlone.interfaces import INonInstallable \
    as INonInstallableProfiles

from plonesymposium.southamerica.config import PRODUCTS
from plonesymposium.southamerica.config import PROJECTNAME


def get_package_name(name):
    return name[9:] if name.startswith('Products') else name


class HiddenProducts(grok.GlobalUtility):

    grok.implements(INonInstallableProducts)
    grok.provides(INonInstallableProducts)
    grok.name(PROJECTNAME)

    def getNonInstallableProducts(self):
        products = []
        if not bool(Globals.DevelopmentMode):
            products = [get_package_name(p['package'])
                for p in PRODUCTS if p['hidden']]
        return products


class HiddenProfiles(grok.GlobalUtility):

    grok.implements(INonInstallableProfiles)
    grok.provides(INonInstallableProfiles)
    grok.name(PROJECTNAME)

    def getNonInstallableProfiles(self):
        name = '%s:uninstall' % PROJECTNAME
        profiles = [name]
        if not bool(Globals.DevelopmentMode):
            profiles.extend([p['profile']
                for p in PRODUCTS if p['hidden']])
        return profiles
