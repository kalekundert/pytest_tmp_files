from pytest_tmp_files import *
import pytest, stat

def test_make_files_1(tmp_path):
    make_files(tmp_path, {
        'a': 'apple',
        'b/c': 'banana carrot',
    })

    pa = tmp_path / 'a'
    pbc = tmp_path / 'b' / 'c'

    assert pa.exists()
    assert pa.is_file()
    assert pa.read_text() == 'apple'
    
    assert pbc.exists()
    assert pbc.is_file()
    assert pbc.read_text() == 'banana carrot'

def test_make_files_2(tmp_path, monkeypatch):
    from subprocess import run

    make_files(tmp_path, {
        'greeting.txt': 'hello world',
        'greeting.lnk': {
            'type': 'symlink',
            'target': 'greeting.txt',
        },
        'greeting.sh': {
            'mode': '744',
            'contents': '''\
#!/usr/bin/env sh
cat greeting.lnk
''',
        },
    })

    monkeypatch.chdir(tmp_path)

    # Creating and running a script is a roundabout but orthogonal way to make 
    # sure the files are created properly.

    p = run(['./greeting.sh'], capture_output=True, text=True)

    assert p.stdout == 'hello world'

def test_make_file_assume_text_1(tmp_path):
    p = tmp_path / 'spam.txt'
    make_file(p, 'spam')

    assert p.exists()
    assert p.is_file()
    assert p.read_text() == 'spam'

def test_make_file_assume_text_2(tmp_path):
    p = tmp_path / 'spam.txt'
    make_file(p, {'contents': 'spam'})

    assert p.exists()
    assert p.is_file()
    assert p.read_text() == 'spam'

@pytest.mark.parametrize(
        'meta, expected', [
            ({}, ''),
            ({'contents': 'spam'}, 'spam'),
        ],
)
def test_make_text_file(meta, expected, tmp_path):
    p = tmp_path / 'file.txt'
    make_text_file(p, meta)

    assert p.exists()
    assert p.is_file()
    assert p.read_text() == expected

@pytest.mark.parametrize(
        'meta, expected', [
            ({}, ''),

            # This example comes from:
            # $ echo spam | python -m base64 -
            ({'base64': 'c3BhbQo='}, 'spam\n'),
        ],
)
def test_make_binary_file(meta, expected, tmp_path):
    p = tmp_path / 'file.bin'
    make_binary_file(p, meta)

    assert p.exists()
    assert p.is_file()
    assert p.read_text() == expected

def test_make_hard_link(tmp_path):
    p1 = tmp_path / 'spam.txt'
    p2 = tmp_path / 'spam.lnk'

    make_text_file(p1, {'contents': 'spam'})
    make_hard_link(p2, {'target': 'spam.txt'})

    assert p1.exists()
    assert p2.exists()

    assert p1.is_file()
    assert p2.is_file()

    assert p1.stat().st_nlink == 2
    assert p2.stat().st_nlink == 2

    assert not p1.is_symlink()
    assert not p2.is_symlink()

    assert p1.read_text() == 'spam'
    assert p2.read_text() == 'spam'

def test_make_soft_link(tmp_path):
    p1 = tmp_path / 'spam.txt'
    p2 = tmp_path / 'spam.lnk'

    make_text_file(p1, {'contents': 'spam'})
    make_soft_link(p2, {'target': 'spam.txt'})

    assert p1.exists()
    assert p2.exists()

    assert p1.is_file()
    assert p2.is_file()

    assert p1.stat().st_nlink == 1
    assert p2.stat().st_nlink == 1

    assert not p1.is_symlink()
    assert p2.is_symlink()

    assert p1.read_text() == 'spam'
    assert p2.read_text() == 'spam'

def test_make_fifo(tmp_path):
    p = tmp_path / 'fifo'
    make_fifo(p, {})

    assert p.exists()
    assert p.is_fifo()

def test_make_directory(tmp_path):
    p = tmp_path / 'dir'
    make_directory(p, {})

    assert p.exists()
    assert p.is_dir()
    assert list(p.iterdir()) == []

def test_make_directory_recursive(tmp_path):
    p = tmp_path / 'dir'

    # This example is a bit contrived, because there's no need to use 
    # `make_directory()` to make non-empty directories.  But the point is to 
    # test the recursive algorithm.
    make_directory(p, {
        'contents': {
            'a': {
                'type': 'dir',
                'contents': {
                    'b': {
                        'type': 'dir',
                        'contents': {
                            'c': {
                                'type': 'dir',
                            },
                        },
                    },
                },
            },
        }
    })

    pa = p / 'a'
    pb = pa / 'b'
    pc = pb / 'c'

    assert p.exists()
    assert p.is_dir()
    assert list(p.iterdir()) == [pa]

    assert pa.exists()
    assert pa.is_dir()
    assert list(pa.iterdir()) == [pb]

    assert pb.exists()
    assert pb.is_dir()
    assert list(pb.iterdir()) == [pc]

    assert pc.exists()
    assert pc.is_dir()
    assert list(pc.iterdir()) == []


@pytest.mark.parametrize(
        'mode_str, mode_bits', [
            ('640', (1,1,0, 1,0,0, 0,0,0)),
            ('755', (1,1,1, 1,0,1, 1,0,1)),
        ],
)
def test_set_mode(mode_str, mode_bits, tmp_path):
    p = tmp_path / 'file'
    p.touch()

    set_mode(p, {'mode': mode_str})
    mode = p.stat().st_mode

    assert bool(mode & stat.S_IRUSR) == mode_bits[0]
    assert bool(mode & stat.S_IWUSR) == mode_bits[1]
    assert bool(mode & stat.S_IXUSR) == mode_bits[2]

    assert bool(mode & stat.S_IRGRP) == mode_bits[3]
    assert bool(mode & stat.S_IWGRP) == mode_bits[4]
    assert bool(mode & stat.S_IXGRP) == mode_bits[5]

    assert bool(mode & stat.S_IROTH) == mode_bits[6]
    assert bool(mode & stat.S_IWOTH) == mode_bits[7]
    assert bool(mode & stat.S_IXOTH) == mode_bits[8]

@pytest.mark.parametrize(
        'meta, atime, mtime', [
            # For `mtime` and `atime`, `None` means "original time".
            ({}, None, None),
            ({'atime': '2022-03-11T12:00:00Z'}, 1647000000, None),
            ({'mtime': '2022-03-11T12:00:00Z'}, None, 1647000000),
            ({
                'atime': '2022-03-11T12:00:00Z',
                'mtime': '2022-03-11T12:00:00Z',
             }, 1647000000, 1647000000),
        ],
)
def test_set_utime(meta, mtime, atime, tmp_path):
    p = tmp_path / 'file'
    p.touch()

    if atime is None:
        atime = p.stat().st_atime
    if mtime is None:
        mtime = p.stat().st_mtime

    set_utime(p, meta)

    assert p.stat().st_atime == atime
    assert p.stat().st_mtime == mtime

