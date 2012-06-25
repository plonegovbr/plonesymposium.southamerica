from setuptools import setup, find_packages
import os

version = '1.0'

long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()


def get_install_requirements():
    """ XXX: document me!
    """
    import ConfigParser
    path = os.path.join('src', 'plonesymposium',
                        'southamerica', 'dependencies.txt')
    requirements = []
    defaults = dict(version='')
    config = ConfigParser.ConfigParser(defaults)
    config.read([path])
    for section in config.sections():
        version = config.get(section, 'version')
        if version and version[0].isdigit():
            version = '==' + version
        requirements.append('%s%s' % (section, version))
    return requirements

setup(name='plonesymposium.southamerica',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Development Status :: 3 - Alpha",
        # XXX: Replace Development Status if needed:
        # "Development Status :: 4 - Beta",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Zope2",
        "License :: Other/Proprietary License",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone plonegovbr plonesymposium web event conference',
      author='PloneGov.Br <gov@plone.org.br>',
      author_email='gov@plone.org.br',
      url='https://github.com/plonegovbr/plonesymposium.southamerica',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['plonesymposium'],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools'] + get_install_requirements(),
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
