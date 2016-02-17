#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Generate Sphinx source files
"""

from pathlib import Path

import winshell

from .config import SPHINX_SOURCES


def generate_prjct_docs(export_path=(SPHINX_SOURCES + '\docs')):
    """ Generates prjct's included documentation sources, and exports it to the
        `export_path`.
    """

    here = Path(__file__)
    readme_loc = here.parent / '..' / 'README.rst'

    docs_files = [readme_loc]

    export_loc = Path.cwd() / export_path / '.no-file'
    # make the folder if it doesn't exist
    export_loc.parent.mkdir(exist_ok=True)

    for my_file in docs_files:
        # with Python 3.5.2 use `readme_loc.path`
        dest_loc = export_loc.with_name(my_file.name)
        winshell.copy_file(str(my_file), str(dest_loc))
