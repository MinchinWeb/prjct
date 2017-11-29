#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
prjct: Project Management for Living Life

Command Line Interface
"""

from pathlib import Path

import click
import invoke
import yaml

from . import config as prjct_config
from . import sphinx as prjct_sphinx
from . import __title__, __version__, multi_source

# TODO: switch over to run shell commands directly from click ??

@click.group()
@click.pass_context
@click.version_option(__version__, prog_name=__title__)
def main(ctx, **kwag):
    pass


@main.command()
@click.pass_context
def sphinx(ctx):
    if prjct_config.confirm():
        cfg = prjct_config.load()
        try:
            invoke.run('del {}\\*.rst'.format(cfg['sphinx']['doc_sources']))
        except invoke.exceptions.Failure:
            pass
        try:
            invoke.run('del {}\\*.rst'.format(cfg['sphinx']['project_sources']))
        except invoke.exceptions.Failure:
            pass
        prjct_sphinx.generate_prjct_docs()
        prjct_sphinx.geneate_projects_page()
        prjct_sphinx.generate_project_summaries(cfg['sphinx']['jrnl_sources'])
    else:
        print('No existing configuration file found. Default configuration \
              written to\n{}\nPlease reveiw configuration and re-run.'\
              .format(prjct_config.file_path()))


@main.command()
@click.pass_context
def jrnl(ctx):
    if prjct_config.confirm():
        cfg = prjct_config.load()

        # make the directory if it doesn't exist
        Path(cfg['sphinx']['jrnl_sources']).mkdir(exist_ok=True)

        try:
            invoke.run('del {}\\*.md'.format(cfg['sphinx']['jrnl_sources']))
        except invoke.exceptions.Failure:
            pass

        for journal in cfg['jrnl']['journals']:
            invoke.run('jrnl {} --export prjct -o {}'
                       .format(journal, cfg['sphinx']['jrnl_sources']))
    else:
        print("No existing configuration file found. Default configuration "
              "written to\n{}\nPlease reveiw configuration and re-run."
              .format(prjct_config.file_path()))


@main.command()
@click.pass_context
def build(ctx):
    invoke.run('make dirhtml')
    # set `pty` to True for colour output, but that's no supported on Windows :(


@main.command()
@click.pass_context
def config(ctx):
    """
    Prints the location of the configuration files. If none is found, the
    default is written to disk.
    """
    cfg = prjct_config.load_or_install_prjct()

    print("Configuration for {}, v.{}".format(__title__, __version__))
    print("    located at {}".format(prjct_config.CONFIG_FILE_PATH))
    print()
    print(yaml.dump(cfg, indent=4, default_flow_style=False))


@main.command()
@click.pass_context
@click.argument('output', type=click.File('w'))
def project_entry(ctx, output):
    """Create an entry listing all projects defined."""
    output.write(multi_source.all_projects_entry())
    print('[All Projects Entry exported to {}]'.format(output.name))


@main.command()
@click.pass_context
def z(ctx):
    prjct_sphinx.geneate_projects_page()
