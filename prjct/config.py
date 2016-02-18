#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Configuration for prjct
"""

# module constants
COMPLETION_CUTOFF = 30  # only dispaly done items completed in this many days
TODO_SORT_STRING = 'desc:done,desc:importance,due,desc:priority,asc:creation'
SPHINX_SOURCES = 'source'
SPHINX_DOC_SOURCES = SPHINX_SOURCES + '\docs'
SPHINX_JRNL_SOURCES = SPHINX_SOURCES + '\jrnl'
SPHINX_PROJECT_SOURCES = SPHINX_SOURCES + '\projects'
JOURNALS = ['default', 'dayone']
