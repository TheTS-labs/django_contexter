# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

PROJECT = "Friendly Contexter"
COPYRIGHT = "2022, Roman"
AUTHOR = "Roman"
REELASE = "0.4.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

EXTENSIONS = [
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
]

TEMPLATES_PATH = ["_templates"]
EXCLUDE_PATTERNS = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
HTML_STATIC_PATH = ["_static"]
