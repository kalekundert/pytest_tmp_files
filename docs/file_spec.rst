******************
File specification
******************

File hierarchies are specified using dictionaries, where the keys specify file 
paths and the values specify file contents.  

The paths (keys) must always be strings.  The paths may contain directories and 
subdirectories that don't exist yet; any necessary directories will be created 
automatically.

The contents (values) can be either strings or dictionaries.  Strings are used 
for simple text files; the given text will be written to the file verbatim.  
This is by far the most common way to specify file contents.  Dictionaries are 
used when more control is required, e.g. to create symlinks, to use non-default 
file permissions, etc.  The fields expected in these dictionaries depends on 
the type of file being created, as documented below:

Text files
==========
Text files can be specified either as strings, or as dictionaries with the 
following keys:

- ``"type"`` (optional): ``"text"``
- ``"content"`` (optional): The text to write to the file.  If not specified, 
  the file will be empty.
- ``"mode"`` (optional): An octal number (e.g. 644) describing which permission 
  bits to set for the file.  This value is passed on to 
  :meth:`pathlib.Path.chmod`, so refer to that documentation for the precise 
  meaning of these bits.
- ``"atime"`` (optional): The date and time when the file was most recently 
  accessed, as an ISO-formatted string.  By default, this will be the current 
  time.
- ``"mtime"`` (optional): The date and time when the file was most recently 
  modified, as an ISO-formatted string.  By default, this will be the current 
  time.

**Examples:**

A file named ``spam.txt`` containing the string ``eggs`` (specified several 
equivalent ways):

.. code-block::

  {'spam.txt': 'eggs'}

.. code-block::

  {'spam.txt': {'content': 'eggs'}}

.. code-block::

  {'spam.txt': {'type': 'text', 'content': 'eggs'}}

A user-executable file:

.. code-block::

  {'spam.sh': {'mode': '744', 'content': '#!/usr/bin/env sh\necho eggs'}}

A file that was last modified on a specific date:

.. code-block::

  {'spam.txt': {'mtime': '2022-03-11', 'content': 'eggs'}}

Binary files
============
Binary files can be specified as dictionaries with the following keys:

- ``"type"`` (required): ``"bin"``
- ``"base64"`` (optional): The base-64 encoded contents of the file.text to 
  write to the file.  If not specified, the file will be empty.
- ``"mode"`` (optional): See `Text files`_.
- ``"atime"`` (optional): See `Text files`_.
- ``"mtime"`` (optional): See `Text files`_.

**Example:**

A PNG file:

.. code-block::

  {'emoji.png': {'type': 'bin', 'base64': 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII='}}

Soft links
==========
Soft links (a.k.a. symlinks) can be specified as dictionaries with the 
following keys:

- ``"type"`` (required): ``"symlink"``
- ``"target"`` (required): The path that the file should link to, relative to 
  the file itself.
- ``"mode"`` (optional): See `Text files`_.
- ``"atime"`` (optional): See `Text files`_.
- ``"mtime"`` (optional): See `Text files`_.

**Examples:**

A symlink to a file in the same directory:

.. code-block::

  {
    'spam.txt': 'eggs',
    'spam.lnk': {'type': 'symlink', 'target': 'spam.txt'},
  }

A symlink to a file in a different directory:

.. code-block::

  {
    'a/spam.txt': 'eggs',
    'b/spam.lnk': {'type': 'symlink', 'target': '../a/spam.txt'},
  }

Hard links
==========
Hard links (a.k.a. links) can be specified as dictionaries with the following 
keys:

- ``"type"`` (required): ``"link"``
- ``"target"`` (required): The path that the file should link to, relative to 
  the file itself.
- ``"mode"`` (optional): See `Text files`_.
- ``"atime"`` (optional): See `Text files`_.
- ``"mtime"`` (optional): See `Text files`_.

**Examples:**

A hard link to a file in the same directory:

.. code-block::

  {
    'spam.txt': 'eggs',
    'spam.lnk': {'type': 'link', 'target': 'spam.txt'},
  }

A hard link to a file in a different directory:

.. code-block::

  {
    'a/spam.txt': 'eggs',
    'b/spam.lnk': {'type': 'link', 'target': '../a/spam.txt'},
  }

Named FIFOs
===========
Named FIFOs can be specified as dictionaries with the following keys:

- ``"type"`` (required): ``"fifo"``
- ``"mode"`` (optional): See `Text files`_.
- ``"atime"`` (optional): See `Text files`_.
- ``"mtime"`` (optional): See `Text files`_.

Directories
===========
Directories can be specified as dictionaries with the following keys:

- ``"type"`` (required): ``"dir"``
- ``"contents"`` (optional): A dictionary with the same format as the top-level 
  dictionary (i.e. the one specifying the whole file hierarchy), except that 
  the paths (keys) are now relative to this directory.  These directory 
  dictionaries can be nested any number of times.
- ``"mode"`` (optional): See `Text files`_.
- ``"atime"`` (optional): See `Text files`_.
- ``"mtime"`` (optional): See `Text files`_.

Note that it's only necessary to specify a directory like this if you want an 
empty directory.  Otherwise, it's easier just the specify the path the file you 
want, and all of the directories along that path will be created automatically.

**Example:**

An empty directory:

.. code-block::

  {'empty': {'type': 'dir'}}

A directory containing a text file.  Note that the directory does not need to 
be specified separately from the file itself:

.. code-block::

  {'dir/spam.txt': 'eggs'}

Need something else?
====================
If you need some kind of file that isn't currently supported, please feel free 
to open a `bug report`_ describing your situation.  I'd like this library to 
support as many use-cases as possible!  Alternatively, you can add use the 
`tmp_file_type` decorator to define your own custom file types.

.. _`bug report`: https://github.com/kalekundert/pytest_tmp_files/issues
