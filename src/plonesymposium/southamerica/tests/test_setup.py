# -*- coding: utf-8 -*-
import unittest2 as unittest

from zope.site.hooks import setSite

from zope.component import getUtility

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.testing import setRoles

from plonesymposium.southamerica.quickinstaller import get_package_name
from plonesymposium.southamerica.testing import INTEGRATION_TESTING

PROJECTNAME = 'plonesymposium.southamerica'


class BaseTestCase(unittest.TestCase):
    """base test case to be used by other tests"""

    layer = INTEGRATION_TESTING

    def setUpUser(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(self.portal, TEST_USER_NAME)

    def setUp(self):
        portal = self.layer['portal']
        setSite(portal)
        self.portal = portal
        self.qi = getattr(self.portal, 'portal_quickinstaller')
        self.pp = getattr(self.portal, 'portal_properties')
        self.wt = getattr(self.portal, 'portal_workflow')
        self.st = getattr(self.portal, 'portal_setup')
        self.setUpUser()


class TestInstall(BaseTestCase):
    """ensure product is properly installed"""

    def test_installed(self):
        self.failUnless(self.qi.isProductInstalled(PROJECTNAME),
                        '%s not installed' % PROJECTNAME)

    def test_base_dependencies_installed(self):
        for p in PRODUCTS:
            name = get_package_name(p['package'])
            self.assertTrue(self.qi.isProductInstalled(name),
                            '%s not installed' % name)


class TestConfig(BaseTestCase):
    """ Ensure we have configured this portal """

    def test_title(self):
        self.failUnless(self.portal.title.startswith('Tribunal Regional'),
                        'Title not applied')

    def test_email_configs(self):
        self.failUnless(self.portal.email_from_address,
                        'E-mail address not set')
        self.failUnless(self.portal.email_from_name,
                        'E-mail name not set')

    def test_localTimeFormat(self):
        self.failUnless(self.pp.site_properties.localTimeFormat == '%d/%m/%Y',
                        'Time format not set')

    def test_allowed_combined_language_code(self):
        self.lang = getattr(self.portal, 'portal_languages')
        self.failUnless(self.lang.use_combined_language_codes == 1,
                        'Combined language code not supported')

    def test_language_set(self):
        self.lang = getattr(self.portal, 'portal_languages')
        self.failUnless(self.lang.getDefaultLanguage() == 'pt-br',
                        'Language not set')

    def test_hidden_home(self):
        self.actions = getattr(self.portal, 'portal_actions')
        portal_tabs = self.actions['portal_tabs']
        self.failIf(portal_tabs['index_html'].visible,
                        'Home tab still visible')

    def test_content_rules_installed(self):
        from zope.component.interfaces import IObjectEvent
        from plone.contentrules.rule.interfaces import IRuleAction
        element = getUtility(IRuleAction,
                             name='sc.contentrules.actions.groupbydate')
        self.assertEquals('sc.contentrules.actions.groupbydate',
                          element.addview)
        self.assertEquals('edit', element.editview)
        self.assertEquals(None, element.for_)
        self.assertEquals(IObjectEvent, element.event)


class TestUninstall(BaseTestCase):
    """ensure product is properly uninstalled"""

    def setUp(self):
        BaseTestCase.setUp(self)
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.failIf(self.qi.isProductInstalled(PROJECTNAME))


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
