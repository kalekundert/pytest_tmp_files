pytest_plugins = ['pytester']

def test_tmp_files_indirect(testdir):
    testdir.makefile('.py', """\
            import pytest

            @pytest.mark.parametrize(
                    'tmp_files, expected', [
                            ({'file.txt': 'spam'}, 'spam'),
                            ({'file.txt': 'eggs'}, 'not eggs'),
                    ],
                    indirect=['tmp_files'],
            )
            def test_open(tmp_files, expected):
                with open(tmp_files / 'file.txt') as f:
                    assert f.read() == expected
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1, failed=1)

def test_tmp_files_manifest(testdir):
    testdir.makefile('.py', """\
            import pytest

            MANIFEST = {
                    'a': 'a',
                    'b/c': 'bc',
            }

            @pytest.mark.parametrize(
                    'tmp_files', [MANIFEST],
                    indirect=True,
            )
            def test_open(tmp_files):
                assert (tmp_files / 'a').read_text() == 'a'
                assert (tmp_files / 'b' / 'c').read_text() == 'bc'
                assert tmp_files.manifest == MANIFEST
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

