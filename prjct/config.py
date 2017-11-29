#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""Configuration for prjct."""

import logging
import os
from pathlib import Path

import xdg.BaseDirectory  # packaged as pyxdg
import yaml  # packaged at pyyaml

from . import __version__
from .util import sort_project_list

log = logging.getLogger(__name__)

# TODO: Can we pull invoke's config and use it here?
#       That is set up to allow nested configuration, and configuaration using
#       YAML, JSON, or py files.
#       http://docs.pyinvoke.org/en/0.13.0/concepts/configuration.html
#       https://github.com/pyinvoke/invoke/blob/master/invoke/config.py

# TODO: deal with versioning, and updating on version updates

# TODO: add default configuration, so it doesn't break if values aren't
#       provided

# TODO: consider replacing `reyaml` with `pyyaml` (but then we lose comments)


DEFAULT_CFG_FILE = 'prjct.yaml'
XDG_RESOURCE = 'prjct'

USER_HOME = os.path.expanduser('~')

CONFIG_PATH = xdg.BaseDirectory.save_config_path(XDG_RESOURCE) or USER_HOME
CONFIG_FILE_PATH = os.path.join(CONFIG_PATH, DEFAULT_CFG_FILE)


MARKDOWN_EXT = ['.md', ]


default_cfg = {
    'version': __version__,
    'todo': {
        # in days; items completed beyond this aren't listed
        'completion_cutoff': 30,
        'sort_string': 'desc:done,desc:importance,due,desc:priority,asc:creation',
    },
    'sphinx': {
        'doc_source': 'sources\docs',
        'jrnl_sources': 'sources\jrnl',
        'project_sources': 'sources\projects',
    },
    # can be an absolute or relative path
    # if a relative path is given, it is relative to this file
    'descriptions_dir': 'descriptions',
    # which journals should be included
    'jrnl': {
        'journals': 'default',
    },
    'export': {
        'all_projects_date': '2012-01-01',
    },
    'someday_projects': None,
    'completed_projects': None,
}


def upgrade_config(cfg):
    """
    Checks if there are keys missing in a given config dict, and if so, updates
    the config file accordingly. This essentially automatically ports prjct
    installations if new config parameters are introduced in later versions.
    """
    missing_keys = set(default_cfg).difference(cfg)
    if missing_keys or cfg['version'] != __version__:
        for key in missing_keys:
            cfg[key] = default_cfg[key]
        save_config(cfg)
        print("[Configuration updated to newest version at {}]".format(CONFIG_FILE_PATH))


def save_config(cfg):
    cfg['version'] = __version__
    with open(CONFIG_FILE_PATH, 'w') as f:
        yaml.safe_dump(cfg, f, encoding='utf-8', allow_unicode=True, default_flow_style=False)


def load_config(config_path):
    """Tries to load a config file from YAML."""
    with open(config_path) as f:
        return yaml.load(f)


def load_or_install_prjct():
    """
    If prjct is already installed, loads and returns a config object.
    Else, perform various prompts to install prjct.
    """
    config_path = CONFIG_FILE_PATH
    if os.path.exists(config_path):
        log.debug('Reading configuration from file %s', config_path)
        cfg = load_config(config_path)
        # upgrade.upgrade_prjct_if_necessary(config_path)
        upgrade_config(cfg)
        return cfg
    else:
        log.debug('Configuration file not found, installing prjct...')
        return install()


def install():
    # def autocomplete(text, state):
    #     expansions = glob.glob(os.path.expanduser(os.path.expandvars(text)) + '*')
    #     expansions = [e + "/" if os.path.isdir(e) else e for e in expansions]
    #     expansions.append(None)
    #     return expansions[state]

    # readline.set_completer_delims(' \t\n;')
    # readline.parse_and_bind("tab: complete")
    # readline.set_completer(autocomplete)

    # # Where to create the journal?
    # path_query = 'Path to your journal file (leave blank for {}): '.format(JOURNAL_FILE_PATH)
    # journal_path = util.py23_input(path_query).strip() or JOURNAL_FILE_PATH
    # default_config['journals']['default'] = os.path.expanduser(os.path.expandvars(journal_path))

    # path = os.path.split(default_config['journals']['default'])[0]  # If the folder doesn't exist, create it
    # try:
    #     os.makedirs(path)
    # except OSError:
    #     pass

    # PlainJournal._create(default_config['journals']['default'])

    cfg = default_cfg
    save_config(cfg)
    return cfg


def someday_projects():
    """
    Return a list of "someday" projects.

    These tend to be projects that aren't under active progressions at the
    moment, and also haven't been completed.
    """
    cfg = load_or_install_prjct()
    someday_projects_list = cfg['someday_projects'] if cfg['someday_projects'] else []
    return sort_project_list(someday_projects_list)


def completed_projects():
    """
    Return a list of "completed" projects.

    These are projects deemed completed (at least for now).
    """
    cfg = load_or_install_prjct()
    completed_projects_list = cfg['completed_projects'] if cfg['completed_projects'] else []
    return sort_project_list(completed_projects_list)


def project_list():
    """
    Create a list of projects from the configuration.

    Merges the projects lists from the configuration of someday and completed
    projects.
    """
    cfg = load_or_install_prjct()

    completed_projects_list = set(cfg['completed_projects'] if cfg['completed_projects'] else [])
    someday_projects_list = set(cfg['someday_projects'] if cfg['someday_projects'] else [])

    # operator called 'join' and gives the union of the two sets
    all_projects_list = list(completed_projects_list | someday_projects_list)
    return sort_project_list(all_projects_list)
