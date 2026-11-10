# Code Review — Mopidy-dLeyna 3.0.0

**Date:** 2026-11-10
**Reviewed:** `develop`, i.e. `master` at `6ab23ef` ("Bump actions/setup-python from
6.2.0 to 6.3.0", v3.0.0 plus dependency bumps) plus the build environment update, the
fixes for client errors, D-Bus shutdown logging and object paths and this review
commit; `__version__` 3.0.0.

**CI status:** All default `tox` environments pass locally on CPython 3.13.18 (`py`:
51 passed) with Mopidy 4.0.5; not run on 3.14 locally and not against a real dLeyna
server. GitHub Actions is green on 3.13 and 3.14 for `develop` before this review
commit. `tox -e pyright` fails with 59 errors (Code #1). **Coverage:** 59 % with
branches; `translator.py` and `playback.py` are at 100 %, `library.py` at 92 %, but
`backend.py` (0 %), `client.py` (27 %) and `util.py` (60 %) are barely exercised,
since `dbus` is stubbed in tests.

## Code — Potential Issues

| # | Priority | Location | Finding |
|---|----------|----------|---------|
| 1 | Low | whole package, `tests/` | pyright `standard` reports 59 errors: Mopidy 4's typed models (`Uri`, `ReleaseDate`, `DurationMs`, `tuple` artists and search results) reject plain values, `self.backend.client` is unknown on `backend.Backend`, `root_directory.uri` is optional, and `dbus` cannot be resolved in the tox environment. Blocks adding `pyright` to the envlist. |

## Tests — Gaps

| # | Priority | Finding |
|---|----------|---------|
| 1 | Low | `dLeynaBackend` (session bus detection, start and stop), `dLeynaClient` (`SortCaps` filtering, `Servers` signals; only `urimapper` is tested) and `util.Future.fromdbus()` have no tests. |
| 2 | Low | `iterate()` ending a listing on an error after the first page (line 52) is untested; `tests/test_errors.py` covers errors on the first page only. |
| 3 | Info | Two `DeprecationWarning`s come from `mopidy.types` at import time, not from this package. |

## Changelog

| # | Priority | Finding |
|---|----------|---------|
| 1 | Medium | The next release's entry needs a line for the changed behavior, e.g. "Log errors and return empty results from ``browse()``, ``lookup()``, ``get_images()`` and ``search()`` instead of raising." and "Log D-Bus daemon shutdown at info level.", plus "Update build environment." for the ruff, `tox` and CI changes and the removal of `setup.cfg` and `setup.py`. |
