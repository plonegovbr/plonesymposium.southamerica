# -*- coding: utf-8 -*-
import logging
from collective.grok import gs
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.upgrade import listUpgradeSteps

_PROJECT = 'plonesymposium.southamerica'
_PROFILE_ID = 'plonesymposium.southamerica:default'


# TODO: move this to another place
def get_package_dependencies():
    """ XXX: document me!
    """
    import os
    import ConfigParser
    dependencies = []
    path = os.path.join(os.path.dirname(__file__), 'dependencies.txt')
    defaults = dict(hidden='False', install='False', profile='')
    config = ConfigParser.ConfigParser(defaults)
    config.read([path])
    for p in config.sections():
        hidden = config.getboolean(p, 'hidden')
        install = config.getboolean(p, 'install')
        profile = config.get(p, 'profile')
        if install:
            package = dict(
                package=p, locked=False, hidden=hidden,
                install=install, profile=profile,
                )
            dependencies.append(package)
    return dependencies


# Upgrade steps
@gs.importstep(name="plonesymposium.southamerica-upgrades",
               title="plonesymposium.southamerica: Upgrades",
               description="Run available upgrades for this package.")
def run_upgrades(context):
    """ Run Upgrade steps
    """
    if context.readDataFile('plonesymposium.southamerica-default.txt') is None:
        return
    logger = logging.getLogger(_PROJECT)
    site = context.getSite()
    setup_tool = getToolByName(site, 'portal_setup')
    version = setup_tool.getLastVersionForProfile(_PROFILE_ID)
    upgradeSteps = listUpgradeSteps(setup_tool, _PROFILE_ID, version)
    sorted(upgradeSteps, key=lambda step: step['sortkey'])

    for step in upgradeSteps:
        oStep = step.get('step')
        if oStep is not None:
            oStep.doStep(setup_tool)
            msg = "Ran upgrade step %s for profile %s" % (oStep.title,
                                                          _PROFILE_ID)
            setup_tool.setLastVersionForProfile(_PROFILE_ID, oStep.dest)
            logger.info(msg)
