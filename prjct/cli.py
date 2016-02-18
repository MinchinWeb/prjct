#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
prjct: Project Management for Living Life

Command Line Interface
"""

import click
import invoke

from . import __version__, __title__
from . import sphinx as prjct_sphinx
from.config import JOURNALS, SPHINX_JRNL_SOURCES


@click.group()
@click.pass_context
# @click.argument('workbook_path')  # Data Source (Excel workbook)
# @click.option('--config', default='sample_config',
#              help='Directory containing configuration files.',
#              show_default=True)
# @click.option('-v', '--verbose', count=True,
#              default=0,  # set default so a value gets passed, even if not set by the user
#              help='Display more debugging output. Can be used up to twice.')
#@click.argument('subcommand')
@click.version_option(__version__, prog_name=__title__)
def main(ctx, **kwag):
    pass


@main.command()
@click.pass_context
def sphinx(ctx):
    prjct_sphinx.generate_prjct_docs()
    prjct_sphinx.generate_project_summaries()


@main.command()
@click.pass_context
def jrnl(ctx):
    invoke.run('del {}\\*.md'.format(SPHINX_JRNL_SOURCES))
    for journal in JOURNALS:
        invoke.run('jrnl {} --export prjct -o {}'.format(journal, SPHINX_JRNL_SOURCES))


@main.command()
@click.pass_context
def build(ctx):
    invoke.run('make dirhtml')
    # TODO: this kills the colour output...


# TODO: empty source folders before we run
