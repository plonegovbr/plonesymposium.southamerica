# -*- coding: utf-8 -*-
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles

from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import plonesymposium.southamerica
        self.loadZCML(package=plonesymposium.southamerica)

    def setUpPloneSite(self, portal):
        # create fake content
        setRoles(portal, TEST_USER_ID, ['Manager', 'Editor', 'Reviewer'])
        login(portal, TEST_USER_NAME)
        portal.invokeFactory('Folder', 'news')
        portal.invokeFactory('Folder', 'events')
        portal.invokeFactory('Folder', 'Members')
        portal.invokeFactory('Document', 'front-page')
        logout()
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'plonesymposium.southamerica:default')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='plonesymposium.southamerica:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='plonesymposium.southamerica:Functional',
    )
