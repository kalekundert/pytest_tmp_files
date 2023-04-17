*************************************
Temporary file hierarchies for pytest
*************************************

.. image:: https://img.shields.io/pypi/v/pytest_tmp_files.svg
   :alt: Last release
   :target: https://pypi.python.org/pypi/pytest_tmp_files

.. image:: https://img.shields.io/pypi/pyversions/pytest_tmp_files.svg
   :alt: Python version
   :target: https://pypi.python.org/pypi/pytest_tmp_files

.. image:: https://img.shields.io/readthedocs/pytest_tmp_files.svg
   :alt: Documentation
   :target: https://pytest-tmp-files.readthedocs.io/

.. image:: https://img.shields.io/github/actions/workflow/status/kalekundert/pytest_tmp_files/test.yml?branch=master
   :alt: Test status
   :target: https://github.com/kalekundert/pytest_tmp_files/actions

.. image:: https://img.shields.io/codecov/c/gh/kalekundert/pytest_tmp_files.svg
   :alt: Test coverage
   :target: https://app.codecov.io/gh/kalekundert/pytest_tmp_files

.. image:: https://img.shields.io/github/last-commit/kalekundert/pytest_tmp_files?logo=github
   :alt: Last commit
   :target: https://github.com/kalekundert/pytest_tmp_files

``pytest_tmp_files`` is a pytest plugin that provides a fixture for creating 
temporary file hierarchies.  This fixture is called ``tmp_files``, and you can 
think of it as an extension of the built-in ``tmp_path`` fixture.  In addition 
to creating a unique temporary directory for each test, ``tmp_files`` also 
fills in that directory with any files needed for that test.

The files to create are specified by a dictionary provided to fixture via 
`indirect parametrization`_.  For example, here's a test for a function that 
searches for files whose contents match a given regular expression:

.. code-block:: python

  import pytest, re
  from pathlib import Path

  def find_text(top, pattern):
      hits = set()

      for path in Path(top).glob('**/*'):
          if path.is_file() and re.search(pattern, path.read_text()):
              hits.add(path)

      return hits

  @pytest.mark.parametrize(
      'tmp_files, pattern, expected', [
          ({'a': 'x'}, 'x', {'a'}),
          ({'a': 'x'}, 'y', set()),
          ({'a/b': 'x'}, 'x', {'a/b'}),
          ({'a/b': 'x'}, 'y', set()),
          ({'a/b': 'x', 'c': 'y'}, 'x', {'a/b'}),
          ({'a/b': 'x', 'c': 'y'}, 'y', {'c'}),
          ({'a/b': 'x', 'c': 'y'}, '[xy]', {'a/b', 'c'}),
      ],
      indirect=['tmp_files'],
  )
  def test_find_text(tmp_files, pattern, expected):
      expected = {
              tmp_files / p
              for p in expected
      }
      assert find_text(tmp_files, pattern) == expected

The first parameter in each set (the dictionary) specifies the files to create.  
The keys are file paths and the values are file contents, so ``{'a/b': 'x'}`` 
specifies a subdirectory ``a`` containing a text file ``b`` with the contents 
``x``.  Although not shown here, it's also possible to create different kinds 
of files (e.g. binary files, symlinks, hard links, named FIFOs) and to specify 
file metadata (e.g. permissions, modification times).

If this plugin sounds useful to you, you may also be interested in `Parametrize 
From File`_.  These two packages work really well together, because 
``tmp_files`` lends itself to long, multi-line parameters and *Parametrize From 
File* makes such parameters easier to manage.

.. _`indirect parametrization`: https://docs.pytest.org/en/latest/example/parametrize.html#indirect-parametrization
.. _documentation: https://pytest-tmp-files.readthedocs.io/
.. _`Parametrize From File`: https://parametrize-from-file.readthedocs.io/

Check out the documentation_ for more information.

