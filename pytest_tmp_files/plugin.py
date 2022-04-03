import pytest
from .make import make_files

@pytest.fixture
def tmp_files(request, tmp_path):
    """
    An extension of :std:fixture:`tmp_path` that can create a temporary file 
    hierarchy when indirectly parametrized.

    In order to use this fixture, simply specify *tmp_files* as an argument to 
    any of your test functions.  There's no need to import anything; this 
    plugin installs itself so that pytest will automatically be able to find 
    this fixture.

    You must use `indirect parametrization`_ to specify which files to create.  
    Any dictionary matching the format described :doc:`here </file_spec>` can be used 
    as a parameter.  Here an example of what this looks like:

    .. code-block:: python

        import pytest

        @pytest.mark.parametrize(
            'tmp_files, ...', [
                ({'path/to/file': 'file contents'}, ...),
                ...
            ],
            indirect=['tmp_files'],
        )
        def test_my_function(tmp_files, ...):
            ...

    Note the *indirect* argument.  This specifies that the *tmp_files* 
    parameters should be made available to the `tmp_files` fixture.  Also note 
    that each set of parameters will get its own file hierarchy.  This is good 
    for making each test independent from all the others.

    If you don't want to use parametrization (e.g. if you only have one 
    scenario you want to test), you probably don't want to use this fixture.  
    Instead, use the :std:fixture:`tmp_path` fixture and call `make_files` 
    within the test function to create your file hierarchy.

    .. _`indirect parametrization`: https://docs.pytest.org/en/latest/example/parametrize.html#indirect-parametrization
    """

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
