# -*- coding: utf-8 -*-
import logging

from collective.grok import gs
from Products.CMFCore.utils import getToolByName

from plonesymposium.southamerica.config import PRODUCTS
from plonesymposium.southamerica.config import PROJECTNAME
from plonesymposium.southamerica.quickinstaller import get_package_name


@gs.upgradestep(title=u'Installs base packages',
                description=u'Base configuration for our site',
                source='0.0', destination='1000', sortkey=1,
                profile='plonesymposium.southamerica:default')
def fromZero(context):
    """ Upgrade from Zero to version 1000
    """
    jstool = getToolByName(context, 'portal_javascripts')
    csstool = getToolByName(context, 'portal_css')
    ksstool = getToolByName(context, 'portal_kss')
    portal = getToolByName(context, 'portal_url').getPortalObject()
    qi = getToolByName(context, 'portal_quickinstaller')

    # Desabilita modo de debug do js, css e kss
    dmode = False
    jstool.setDebugMode(dmode)
    csstool.setDebugMode(dmode)
    ksstool.setDebugMode(dmode)

    # Remove default content
    fix_default_content(portal)

    for p in PRODUCTS:
        qi.installProduct(get_package_name(p['package']), locked=p['locked'],
                          hidden=p['hidden'], profile=p['profile'])


def fix_default_content(portal):
    """ Clean up default content types
        Reindex created objects
    """
    logger = logging.getLogger(PROJECTNAME)
    content_ids = ['front-page', 'events', ]
    portal_ids = portal.objectIds()
    for cId in content_ids:
        if cId in portal_ids:
            portal.manage_delObjects([cId])
            logger.info('Deleted object with id %s' % cId)
    if 'news' in portal_ids:
        news = portal['news']
        news.setTitle(u'Notícias')
        news.setDescription(u'Notícias do Plone Symposium')
        news.reindexObject()
    if 'members' in portal_ids:
        # Hide user's tab
        members = portal['members']
        members.setExcludeFromNav(True)
        members.reindexObject()

    logger.info('Cleaned up portal contents')
