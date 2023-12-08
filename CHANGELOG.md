# CHANGELOG



## v0.0.2 (2023-12-08)

### Chore

* chore: fix action name ([`7969f40`](https://github.com/kalekundert/pytest_tmp_files/commit/7969f40fb1dac458a2e4cf3a9c6bbe7d0ae28177))

* chore: update checkout and setup-python actions ([`6695809`](https://github.com/kalekundert/pytest_tmp_files/commit/6695809f08c1ecb73f9562a71d34085171d28215))

* chore: test the latest version of python ([`bea1daf`](https://github.com/kalekundert/pytest_tmp_files/commit/bea1daf76eb785a174da5eccb771e9767cef26e7))

* chore: ignore deprecation warnings caused by datetime/dateutil ([`cce2afa`](https://github.com/kalekundert/pytest_tmp_files/commit/cce2afa02159383a2672ee89ad0151fc079facf7))

* chore: switch to gitlint ([`8836772`](https://github.com/kalekundert/pytest_tmp_files/commit/88367725ed5ca5d58840ed47a003099bad192082))

* chore: fix coverage

For some reason, the `pytest-cov` plugin undercounts coverage (specifically: not counting top-level statements), while the `coverage` command itself gives correct results. ([`df94f35`](https://github.com/kalekundert/pytest_tmp_files/commit/df94f3560abf2f45d3bd4ea86257ecadc81c904b))

### Documentation

* docs: fix more documentation links

Fixes #2 ([`99514c3`](https://github.com/kalekundert/pytest_tmp_files/commit/99514c394281cf19e3c7388724a8e74f10817776))

* docs: fix documentation links ([`984bed3`](https://github.com/kalekundert/pytest_tmp_files/commit/984bed371fe064cbc7bc8271c5da29343e9d2f6e))

* docs: fix CI badge ([`4dcb634`](https://github.com/kalekundert/pytest_tmp_files/commit/4dcb634b0cd9a2f5a580f6e1806a7b8574db39b8))

* docs: replace the JSON example with the XLSX example ([`f8a2ac1`](https://github.com/kalekundert/pytest_tmp_files/commit/f8a2ac1bd0d8c8f4069b761fa49abeeeaa3508c9))

* docs: add link to Parametrize From File ([`138de52`](https://github.com/kalekundert/pytest_tmp_files/commit/138de5291bca4002d1f5c4d093c35dbb8993a8fe))

* docs: describe the manifest attribute ([`64a19e1`](https://github.com/kalekundert/pytest_tmp_files/commit/64a19e17e7744b982d7e8c6cd7005912d6dd4a61))

* docs: fix typos ([`c53c2a3`](https://github.com/kalekundert/pytest_tmp_files/commit/c53c2a396f56b9c51606fee990e5cc719e39e89c))

* docs: add link to read the docs ([`5b659f1`](https://github.com/kalekundert/pytest_tmp_files/commit/5b659f14b49aa9d1ad1afedde356c4de9f1f47f9))

### Fix

* fix: don&#39;t use private pathlib methods ([`e4c98fa`](https://github.com/kalekundert/pytest_tmp_files/commit/e4c98fac7320f4db3b8bd9998521fdc5e8504a38))


## v0.0.1 (2022-04-03)

### Chore

* chore: add python 3 trove classifier ([`4046a56`](https://github.com/kalekundert/pytest_tmp_files/commit/4046a56f831d66ce3c39235d654d4579612be711))

* chore: add pytest dependency ([`c76872f`](https://github.com/kalekundert/pytest_tmp_files/commit/c76872fa925afd4d0347de6795211b12d5ffa533))

* chore: apply cookiecutter ([`fe45bfa`](https://github.com/kalekundert/pytest_tmp_files/commit/fe45bfa662bd758997743fa6806758579db91266))

### Documentation

* docs: add API docs ([`7050daf`](https://github.com/kalekundert/pytest_tmp_files/commit/7050dafdeb47e5d1221cf7420764105900846708))

* docs: better title ([`516fd7c`](https://github.com/kalekundert/pytest_tmp_files/commit/516fd7c85664c09351b3e514e3ab3a7a760290ed))

* docs: use syntax highlighting ([`984ddc8`](https://github.com/kalekundert/pytest_tmp_files/commit/984ddc8ea5f21a118b070fc9f4461dadecb2fd28))

* docs: fix link ([`3722841`](https://github.com/kalekundert/pytest_tmp_files/commit/3722841d0feb8d1d0c6b78e3ddd4558ae598002f))

* docs: add README ([`586a471`](https://github.com/kalekundert/pytest_tmp_files/commit/586a4719e0bbf7204299379c734ac34750b68610))

### Fix

* fix: don&#39;t use pathlib to make hard links ([`2ac35bb`](https://github.com/kalekundert/pytest_tmp_files/commit/2ac35bbe8aa3bb26f03955869258c31392e3fe09))

* fix: wrong argument order for Path.link_to() ([`55a29cf`](https://github.com/kalekundert/pytest_tmp_files/commit/55a29cf019d9bedcf90cb822f10113175b0673c7))

### Test

* test: fix doctests ([`f673922`](https://github.com/kalekundert/pytest_tmp_files/commit/f67392222533748a74ddc5fc1df13b49adf265f6))

* test: no need to import `pytest_tmp_files` ([`017899b`](https://github.com/kalekundert/pytest_tmp_files/commit/017899bca71ade29c863abe47d54980b0a7fdc99))

* test: specify UTC timezone for atime/mtime tests ([`58006f8`](https://github.com/kalekundert/pytest_tmp_files/commit/58006f8a925e3a6464d7cd800f99d58b4933182d))

### Unknown

* initial implementation ([`102bd50`](https://github.com/kalekundert/pytest_tmp_files/commit/102bd5036e0366147eb465a032fbf839f1193a0a))
