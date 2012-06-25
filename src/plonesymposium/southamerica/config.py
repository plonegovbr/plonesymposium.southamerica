# -*- coding:utf-8 -*-
import logging

import plonesymposium.southamerica

from collective.grok import gs
from collective.grok import i18n

from sc.policy.helper import deps

from plonesymposium.southamerica.setuphandlers import get_package_dependencies
from plonesymposium.southamerica import MessageFactory as _

PRODUCTS = get_package_dependencies()
PROJECTNAME = 'plonesymposium.southamerica'
PROFILE_ID = 'plonesymposium.southamerica:default'
DEPENDENCIES = deps.get_package_dependencies(plonesymposium.southamerica)
logger = logging.getLogger('plonesymposium.southamerica')


# Default Profile
gs.profile(name=u'default',
           title=_(u'Plone Symposium South America'),
           description=_(u'Installs plonesymposium.southamerica'),
           directory='profiles/default')

# Uninstall Profile
gs.profile(name=u'uninstall',
           title=_(u'Uninstall plonesymposium.southamerica'),
           description=_(u'Uninstall plonesymposium.southamerica'),
           directory='profiles/uninstall')

i18n.registerTranslations(directory='locales')

