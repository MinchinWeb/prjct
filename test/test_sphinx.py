#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Tests the `todo_export.to_html_dicts() function by generate a webpage
containing their results.
"""

import os
import unittest
from pathlib import Path

from prjct.sphinx import generate_prjct_docs


class TestSphinx(unittest.TestCase):

    # TODO: Add setup that removes all files in test/results directory

    def test_generate_docs(self):
        p = Path(__file__)  # location of this file
        output_dir = p.parent / 'results' / 'docs'

        generate_prjct_docs(str(output_dir))

        readme_loc = output_dir / 'README.rst'

        self.assertTrue(os.path.isfile(str(readme_loc)))

if __name__ == "__main__":
    unittest.main()
