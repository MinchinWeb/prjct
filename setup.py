import codecs
import os
import re

import setuptools


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_meta(*meta_file_parts, meta_key):
    """
    Extract __*meta*__ from meta_file
    """
    meta_file = read(*meta_file_parts)
    meta_match = re.search(r"^__{}__ = ['\"]([^'\"]*)['\"]".format(meta_key),
                           meta_file, re.M)
    if meta_match:
        return meta_match.group(1)
    raise RuntimeError("Unable to find __{}__ string.".format(meta_key))


def read_requirements(*parts):
    """
    Given a requirements.txt (or similar style file), returns a list of
    requirements.
    Assumes anything after a single '#' on a line is a comment, and ignores
    empty lines.
    """
    requirements = []
    for line in read(*parts).splitlines():
        new_line = re.sub('(\s*)?#.*$',  # the space immediately before the
                                         # hash mark, the hash mark, and
                                         # anything that follows it
                          '',  # replace with a blank string
                          line)
        new_line = re.sub('(\s*)?-r.*$',  # we also can't reference other
                                          # requirement files
                          '',  # replace with a blank string
                          line)
        if new_line:  # i.e. we have a non-zero-length string
            requirements.append(new_line)
    return requirements


##############################################################################
#                          PACKAGE METADATA                                  #
##############################################################################
META_PATH = ['prjct', '__init__.py']

NAME         = find_meta(*META_PATH, meta_key='title').lower()
VERSION      = find_meta(*META_PATH, meta_key='version')
# SHORT_DESC   = find_meta(*META_PATH, meta_key='description')
SHORT_DESC   = find_meta(*META_PATH, meta_key='tagline')
LONG_DESC    = read('README.rst')
AUTHOR       = find_meta(*META_PATH, meta_key='author')
AUTHOR_EMAIL = find_meta(*META_PATH, meta_key='email')
URL          = find_meta(*META_PATH, meta_key='url')
LICENSE      = find_meta(*META_PATH, meta_key='license')

PACKAGES     = setuptools.find_packages()

# pull from requirements.IN, requirements.TXT is generated from this
INSTALL_REQUIRES = [

    'cloudmesh-timestring',            # timestring>1.6.2
    'topydo>=0.11.0',
    # 'jrnl>=2.0.0rc1',                # updated jrnl is not on PyPI, so vendor...
    'click',
    'invoke',
    'winshell',
    'pypiwin32',                       # pywin32 is required by winshell, but not automatically installed
    'appdirs',
    'markdown',
    'minchin.pelican.jinja_filters',   # for titlecase filter
    'reyaml',                          # switch to PyYAML?

    # jrnl
    "parsedatetime>=1.5",
    "pytz>=2015.7",
    "six>=1.10.0",
    "cryptography>=1.4,<2.0",           # was pinned to 1.4
    "tzlocal>=1.2",
    "pyyaml>=3.11",
    "keyring>=7.3",
    "passlib>=1.6.2",
    "pyxdg>=0.25",
    "asteval>=0.9.8",                   # requires numpy
]

DEV_REQUIRES = read_requirements('requirements-dev.in')

EXTRA_REQUIRES = {
    # conditional requirements for jrnl
    ":python_version<'3.3'": ["monotonic"],
    ":sys_platform == 'win32'" : ["pyreadline>=2.0",     # if readline is unavailable
                                  "colorama>=0.2.5"],
    ":sys_platform != 'win32'" :["readline>=6.2"],       # if readline is unavailable
    ":python_version == '2.6'": ["python-dateutil==1.5"],
    ":python_version == '2.7'": ["python-dateutil==1.5"],
    ":python_version >= '3.0'": ["python-dateutil>=2.2"],

    'build': DEV_REQUIRES,
    'docs': [
        # 'sphinx >= 1.4',  # theme requires at least 1.4
        # 'cloud_sptheme >=1.8',
        # 'releases',
        # 'Babel >=1.3,!=2.0',  # 2.0 breaks on Windows
    ],
    'test': [
        # 'green >=1.9.4',  # v2 works
        # 'coverage',
        # 'isort',
        # 'pydocstyle',
        # 'pycodestyle',
        # 'check-manifest'
    ],
}

# full list of Classifiers at
# https://pypi.python.org/pypi?%3Aaction=list_classifiers
CLASSIFIERS = [
    #   having an unknown classifier should keep PyPI from accepting the
    #   package as an upload
    # 'Private :: Do Not Upload',

    # 'Development Status :: 1 - Planning',
    # 'Development Status :: 2 - Pre-Alpha',
    'Development Status :: 3 - Alpha',
    # 'Development Status :: 4 - Beta',
    # 'Development Status :: 5 - Production/Stable',
    # 'Development Status :: 6 - Mature',
    # 'Development Status :: 7 - Inactive',

    # 'Programming Language :: Python :: 2',
    # 'Programming Language :: Python :: 2.6',
    # 'Programming Language :: Python :: 2.7',
    # 'Programming Language :: Python :: 2 :: Only',
    'Programming Language :: Python :: 3',
    # 'Programming Language :: Python :: 3.2',
    # 'Programming Language :: Python :: 3.3',
    # 'Programming Language :: Python :: 3.4',
    # 'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    # 'Programming Language :: Python :: 3 :: Only',

    'Environment :: Plugins',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Topic :: Documentation',
    'Topic :: Office/Business',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Text Processing',
]
##############################################################################

if LICENSE in ['MIT License']:
    CLASSIFIERS += ['License :: OSI Approved :: {}'.format(LICENSE)]

# add 'all' key to EXTRA_REQUIRES
all_requires = []
for k, v in EXTRA_REQUIRES.items():
    all_requires.extend(v)
EXTRA_REQUIRES['all'] = all_requires


setuptools.setup(
    name=NAME,
    version=VERSION,
    url=URL,
    license=LICENSE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=SHORT_DESC,
    long_description=LONG_DESC,
    packages=PACKAGES,
    package_data={'': ['README.rst',
                       'CHANGELOG.rst',
                       'LICENSE.txt',
                       'requirements.in',
                       'requirements.txt',
                       'requirements-dev.in',
                       'requirements-dev.txt']},
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRA_REQUIRES,
    platforms='any',
    classifiers=CLASSIFIERS,
    # namespace_packages=['prjct',
    #                     ],
    entry_points={
        'console_scripts': [
            'prjct=prjct.cli:main',
            'jrnl = prjct._vendor.jrnl.cli:run',
        ],
    },
)
