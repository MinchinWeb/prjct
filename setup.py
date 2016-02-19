import codecs
import os
import re

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_description = read('readme.rst')


setup(
    name='prjct',
    version=find_version('prjct', '__init__.py'),
    url='http://github.com/minchinweb/prjct',
    license='MIT License',
    author='William Minchin',
    install_requires=['timestring>1.6.2',
                      'topydo',
                      'jrnl>=2.0.0rc1',
                      'ablog>=0.8',
                      'sphinx>=1.3',
                      'releases',
                      'click',
                      'invoke',
                      'winshell',
                      'green',
                      ],
    author_email='w_minchin@hotmail.com',
    description='Project Management for Living Life',
    long_description=long_description,
    packages=['prjct'],
    package_data={'': ['readme.rst', 'changes.rst', 'LICENSE']},
    include_package_data=True,
    platforms='any',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Documentation',
        'Topic :: Office/Business',
        'Topic :: Text Processing',
        ],
    entry_points={
        'console_scripts': ['prjct=prjct.cli:main'],
    }
)
