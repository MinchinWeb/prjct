#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Configuration for prjct."""

from pathlib import Path
import reyaml
import appdirs

# TODO: Can we pull invoke's config and use it here?
#       That is set up to allow nested configuration, and configuaration using
#       YAML< JSON, or py files.
#       http://docs.pyinvoke.org/en/0.13.0/concepts/configuration.html
#       https://github.com/pyinvoke/invoke/blob/master/invoke/config.py

# TODO: deal with versioning, and updating on version updates

# TODO: add default configuration, so it doesn't break if values aren't
#       provided

# TODO: consider replacing `reyaml` with `pyyaml`


CFG_FILE = 'prjct.yaml'
MARKDOWN_EXT = ['.md', ]

'''
# module constants
COMPLETION_CUTOFF = 30  # only dispaly done items completed in this many days
TODO_SORT_STRING = 'desc:done,desc:importance,due,desc:priority,asc:creation'
SPHINX_SOURCES = 'source'
SPHINX_DOC_SOURCES = SPHINX_SOURCES + '\docs'
SPHINX_JRNL_SOURCES = SPHINX_SOURCES + '\jrnl'
SPHINX_PROJECT_SOURCES = SPHINX_SOURCES + '\projects'
JOURNALS = ['default', 'dayone']
ALL_PROJECTS_ENTRY_DATE = '2012-01-01'
'''


def file_path():
    return Path(appdirs.user_config_dir('prjct', 'Minchin')) / CFG_FILE


def confirm():
    """
    Confirm configuration exists.

    This attempts to confirm that the configuration exists as expected. If it
    does not, it writes the default configuration to disk.

    If configuration file exists already, return True. If the congifuration is
    written to disk, return False.
    """
    config_file = file_path()
    # make the folder, if it doesn't exist yet
    config_file.parent.mkdir(exist_ok=True)

    # if the configuration file doesn't exist, write the default
    if not config_file.exists():
        config_file.write_text(r"""\
# This is the configuration file for PRJCT.
# http://www.github.com/MinchinWeb/prjct
# All values are required. This is a YAML formatted file.
 

todo:
    # in days; items completed beyond this aren't listed
    completion_cutoff: 30
    sort_string: 'desc:done,desc:importance,due,desc:priority,asc:creation'

sphinx:
    doc_source: sources\docs
    jrnl_sources: sources\jrnl
    project_sources: sources\projects

# can be an absolute or relative path
# if a relative path is given, it is relative to this file
descriptions_dir: descriptions

# which journals should be included
jrnl:
    journals:
        - default

export:
    all_projects_date: 2012-01-01

someday_projects:

completed_projects:

""")
        return False
    else:
        return True


def load():
    """Load configuration."""
    config_file = file_path()
    cfg = reyaml.load_from_file(str(config_file))

    # add key of the location of the configuration file to the configuration
    # itself
    cfg['file_path'] = str(config_file)

    # TODO: add error checking
    # TODO: add inserting default values
    return cfg
