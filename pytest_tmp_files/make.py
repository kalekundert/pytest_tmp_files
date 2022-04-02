import os, sys

FACTORIES = {}

def tmp_file_type(type):
    def decorator(f):
        FACTORIES[type] = f
        return f
    return decorator


def make_files(root, manifest):
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

    if sys.version_info[:2] >= (3, 10):
        path.hardlink_to(target)
    else:
        path.link_to(target)

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

