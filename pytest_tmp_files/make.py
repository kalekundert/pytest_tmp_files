import os, sys
from pathlib import Path

FACTORIES = {}

# Maybe the factories should be classes.  That would let me associate a schema 
# with each class...

def tmp_file_type(type: str):
    """
    Teach ``pytest_tmp_files`` how to make a new kind of file.

    Arguments:
        type:
            The string that will identify this kind of file in the 
            specification dictionary.

    This function is a decorator.  When a file of the given type is requested, 
    the decorated function will be called with two arguments: *path* and 
    *meta*.  The former is the path to create, and the latter is a free-form
    dictionary containing any user-specified information about the requested 
    file.  These arguments directly correspond to the key and value of an item 
    in the specification dictionary.  The function should create the requested 
    file and return nothing.

    Example:

        The following snippet defines a custom file type called "json".  It 
        expects the metadata to include a "content" field, which it will encode 
        as JSON and write to the indicated path.

        .. code-block::

            >>> from pytest_tmp_files import *
            >>> @tmp_file_type('json')
            ... def make_json_file(path, meta):
            ...     import json
            ...     with open(path, 'w') as f:
            ...         json.dump(meta['content'], f)
            ...

        Here's how this custom file type could be used:

        .. code-block::

            >>> from pathlib import Path
            >>> make_files(Path.cwd(), {
            ...     'demo.json': {
            ...         'type': 'json',
            ...         'content': {'a': 1},
            ...     }
            ... })
            >>> (Path.cwd() / 'demo.json').read_text()
            '{"a": 1}'

        Note that this is just an example; in real applications I'd recommend 
        writing JSON files like this by hand.
    """
    def decorator(f):
        FACTORIES[type] = f
        return f
    return decorator


def make_files(root: Path, manifest: dict):
    """
    Create the file hierarchy specified by the *manifest*.

    Arguments:
        root: 
            The directory where the files will be created.

        manifest:
            A dictionary describing the files to create.  In general, the keys 
            are file paths and the values are file contents.  Refer to the 
            :doc:`/file_spec` for a full description of this dictionary.

    Use this function in cases where the `tmp_files` fixture doesn't make 
    sense.

    Example:

        .. code-block:: pycon

            >>> from pathlib import Path
            >>> from pytest_tmp_files import make_files
            >>> make_files(Path.cwd(), {'dir/greeting.txt': 'hello world!'})
            >>> (Path.cwd() / 'dir' / 'greeting.txt').read_text()
            'hello world!'
    """
    for path, meta in manifest.items():
        make_file(root / path, meta)

def make_file(path, meta):
    if isinstance(meta, str):
        meta = {'type': 'text', 'contents': meta}

    type = meta.get('type', 'text')
    FACTORIES[type](path, meta)

    set_mode(path, meta)
    set_utime(path, meta)

@tmp_file_type('text')
def make_text_file(path, meta):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(meta.get('contents', ''))

@tmp_file_type('bin')
def make_binary_file(path, meta):
    from base64 import b64decode
    b = b64decode(meta.get('base64', ''))

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b)

@tmp_file_type('link')
def make_hard_link(path, meta):
    path.parent.mkdir(parents=True, exist_ok=True)
    target = path.parent / meta['target']

    # Pathlib doesn't get a consistent API for making hard links until python 
    # 3.10, so just use `os.link()` instead.
    os.link(target, path)

@tmp_file_type('symlink')
def make_soft_link(path, meta):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.symlink_to(meta['target'])

@tmp_file_type('fifo')
def make_fifo(path, meta):
    path.parent.mkdir(parents=True, exist_ok=True)
    os.mkfifo(path)

@tmp_file_type('dir')
def make_directory(path, meta):
    path.mkdir(parents=True, exist_ok=True)
    make_files(path, meta.get('contents', {}))

def set_mode(path, meta):
    if 'mode' in meta:
        mode = mode_from_str(meta['mode'])
        path.chmod(mode)

def set_utime(path, meta):
    if 'atime' in meta or 'mtime' in meta:

        if 'atime' in meta:
            atime = timestamp_from_str(meta['atime'])
        else:
            atime = path.stat().st_atime

        if 'mtime' in meta:
            mtime = timestamp_from_str(meta['mtime'])
        else:
            mtime = path.stat().st_mtime

        os.utime(path, (atime, mtime))

def mode_from_str(mode_str):
    return int(mode_str, 8)

def timestamp_from_str(date_str):
    from dateutil.parser import isoparse
    date = isoparse(date_str)
    return date.timestamp()

