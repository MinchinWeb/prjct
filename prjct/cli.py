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
from.config import JOURNALS, SPHINX_JRNL_SOURCES, SPHINX_DOC_SOURCES, SPHINX_PROJECT_SOURCES


@click.group()
@click.pass_context

@click.version_option(__version__, prog_name=__title__)
def main(ctx, **kwag):
    pass


@main.command()
@click.pass_context
def sphinx(ctx):
    invoke.run('del {}\\*.rst'.format(SPHINX_DOC_SOURCES))
    invoke.run('del {}\\*.rst'.format(SPHINX_PROJECT_SOURCES))
    prjct_sphinx.generate_prjct_docs()
    prjct_sphinx.geneate_projects_page()
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
    # set `pty` to True for colour output, but that's no supported on Windows :(


@main.command()
@click.pass_context
def z(ctx):
    prjct_sphinx.geneate_projects_page()
