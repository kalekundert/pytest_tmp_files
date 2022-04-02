import pytest
from .make import make_files

@pytest.fixture
def tmp_files(request, tmp_path):

    # We want to return a `pathlib.Path` instance with an extra `manifest` 
    # attribute that records the specific file names/contents the were 
    # provided.  Unfortunately, `pathlib.Path` uses slots, so the only way to 
    # do this is to make our own subclass.  This is complicated further by the 
    # fact that `pathlib.Path` is just a factory, and instantiates different 
    # classes of objects depending on the operating system.

    class TestPath(type(tmp_path)):
        __slots__ = ('manifest',)

    tmp_path = TestPath._from_parts([tmp_path])
    tmp_path.manifest = request.param

    make_files(tmp_path, request.param)

    return tmp_path
