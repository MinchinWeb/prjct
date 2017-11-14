prjct Changelog
===============

- :release:`0.6.0 <2017-11-13>`
- :support:`-` includes a ``jrnl`` console script that uses the vendorized
  version of ``jrnl``. Also, the vendorized version of ``jrnl`` uses the global
  ``jnrl`` configuration. Therefore, this may cause issues if you install
  ``jrnl`` separately.
- :support:`-` vendorize ``jrnl``; tracks ``prjct`` branch
- :support:`-` adjust ``setup.py`` to make use of ``minchin.releaser``
- :release:`0.5.1 <2017-05-20>`
- :bug:`-` use ``appdirs`` to allow cross-platform placement of config
  directory
- :bug:`-` updated for ``topydo`` v0.11.0
- :feature:`-` render project descriptions files
- :feature:`-` move configuration to external file
- :bug:`-` working version of ``todo_export.to_html_lists()``
- :support:`-` add ``setup.py`` file
- :bug:`-` sort todos intelligently
- :feature:`-` switch from *Pelican* to *Sphinx*
- :release:`0.2.0 <2015-07-20>`
- :support:`-` detail ``jrnl`` and ``todo.txt`` integration
- :release:`0.1.0 <2013-11-30>`
- :support:`-` original conception
