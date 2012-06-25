# -*- coding: utf-8 -*-
import logging

from Products.CMFCore.utils import getToolByName

from s17.app.policy.config import PRODUCTS
from s17.app.policy.config import PROJECTNAME
from s17.app.policy.quickinstaller import get_package_name


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
    remove_default_content(portal)

    # XXX: why we have to do this here if we have metadata.xml?
    for p in PRODUCTS:
        qi.installProduct(get_package_name(p['package']), locked=p['locked'],
                          hidden=p['hidden'], profile=p['profile'])


def remove_default_content(portal):
    """ Clean up default content types
        Reindex created objects
    """
    logger = logging.getLogger(PROJECTNAME)
    content_ids = ['front-page', 'news', ]
    portal_ids = portal.objectIds()
    for cId in content_ids:
        if cId in portal_ids:
            portal.manage_delObjects([cId])
            logger.info('Deleted object with id %s' % cId)

    logger.info('Cleaned up portal contents')
