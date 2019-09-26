#!/usr/bin/env python
# -*- coding: utf-8 -*-

import glob
import os
import subprocess
import sys
from itertools import chain

import sphinx_typlog_theme
from exoplanet_version import __version__  # NOQA

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def setup(app):
    app.add_stylesheet("css/exoplanet.css?v=2019-08-02")


extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.mathjax",
]

autodoc_mock_imports = [
    "numpy",
    "scipy",
    "astropy",
    "pymc3",
    "theano",
    "tqdm",
    "rebound_pymc3",
]

# Convert the tutorials
for fn in chain(
    glob.glob("_static/notebooks/*.ipynb"),
    glob.glob("_static/notebooks/gallery/*.ipynb"),
):
    name = os.path.splitext(os.path.split(fn)[1])[0]
    outfn = os.path.join("tutorials", name + ".rst")
    print("Building {0}...".format(name))
    subprocess.check_call(
        "jupyter nbconvert --template tutorials/tutorial_rst --to rst "
        + fn
        + " --output-dir tutorials",
        shell=True,
    )
    subprocess.check_call("python fix_internal_links.py " + outfn, shell=True)

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://docs.scipy.org/doc/numpy/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "astropy": ("http://docs.astropy.org/en/stable/", None),
}

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

# General information about the project.
project = "exoplanet"
author = "Dan Foreman-Mackey"
copyright = "2018, 2019, " + author

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "exoplanet",
    ),
)

version = __version__
release = __version__

exclude_patterns = ["_build"]
pygments_style = "sphinx"

# HTML theme
html_favicon = "_static/logo.png"
html_theme = "exoplanet"
html_theme_path = ["_themes", sphinx_typlog_theme.get_path()]
html_theme_options = {"logo": "logo.png"}
html_sidebars = {
    "**": ["logo.html", "globaltoc.html", "relations.html", "searchbox.html"]
}
html_static_path = ["_static"]

# Get the git branch name
html_context = dict(
    this_branch="master",
    this_version=os.environ.get("READTHEDOCS_VERSION", "latest"),
)
