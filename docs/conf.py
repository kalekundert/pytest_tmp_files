import sys, os
import pytest_tmp_files

## General

project = 'pytest_tmp_files'
copyright = '2022, Kale Kundert'
version = pytest_tmp_files.__version__
release = pytest_tmp_files.__version__

master_doc = 'index'
source_suffix = '.rst'
templates_path = ['_templates']
exclude_patterns = ['_build']
html_static_path = ['_static']
default_role = 'any'
trim_footnote_reference_space = True
nitpicky = True

## Extensions

extensions = [
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.viewcode',
        'sphinx.ext.intersphinx',
        'sphinx.ext.napoleon',
        'sphinx_rtd_theme',
]
intersphinx_mapping = {
        'python': ('https://docs.python.org/3', None),
        'pytest': ('https://docs.pytest.org/en/stable', None),
}
autosummary_generate = True
autodoc_default_options = {
        'exclude-members': '__dict__,__weakref__,__module__',
}
html_theme = 'sphinx_rtd_theme'
pygments_style = 'sphinx'

def setup(app):
    app.add_crossref_type(
            "fixture",
            "fixture",
            objname="built-in fixture",
            indextemplate="pair: %s; fixture",
    )
