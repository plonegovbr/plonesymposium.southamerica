# encoding: utf-8
from zope.component import adapts

from Products.CMFCore.interfaces import IContentish

from plone.stringinterp.adapters import BaseSubstitution

from plonesymposium.southamerica import MessageFactory as _


class EmailSubstitution(BaseSubstitution):
    adapts(IContentish)

    category = _(u'All Content')
    description = _(u'Content E-mail')

    def safe_call(self):
        return self.context.email


class UIDSubstitution(BaseSubstitution):
    adapts(IContentish)

    category = _(u'All Content')
    description = _(u'Content UID')

    def safe_call(self):
        return self.context.UID()
