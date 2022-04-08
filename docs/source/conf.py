# Configuration file for the Sphinx documentation builder.
import errno
import os
import shutil
import subprocess
import sys
from typing import Set

from natsort import natsorted

docs_dir = os.path.dirname(__file__)
repodir = os.path.abspath(os.path.join(__file__, r"../../.."))
gitdir = os.path.join(repodir, r".git")

# -- Project information -----------------------------------------------------

project = "Merlin"
copyright = "2022, NVIDIA"
author = "NVIDIA"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "myst_nb",
    "sphinx_multiversion",
    "sphinx_rtd_theme",
    "sphinx_markdown_tables",
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_external_toc",
]

# MyST configuration settings
external_toc_path = "toc.yaml"
myst_enable_extensions = [
    "deflist",
    "html_image",
    "linkify",
    "replacements",
    "tasklist",
]
myst_linkify_fuzzy_links = False
myst_heading_anchors = 3
jupyter_execute_notebooks = "off"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    "generated",
]

# Stopgap solution for the moment. Ignore warnings about links to directories.
# In README.md files, the following links make sense while browsing GitHub.
# In HTML, less so.
nitpicky = True
nitpick_ignore = [
    (r"myst", r"./examples/"),
    (r"myst", r"./Deploying-multi-stage-RecSys"),
    (r"myst", r"./getting-started-movielens"),
    (r"myst", r"./scaling-criteo"),
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 3,
}
html_show_sourcelink = False

# Whitelist pattern for tags (set to None to ignore all tags)
# Determine if Sphinx is reading conf.py from the checked out
# repo (a Git repo) vs SMV reading conf.py from an archive of the repo
# at a commit (not a Git repo).
if os.path.exists(gitdir):
    tag_refs = (
        subprocess.check_output(["git", "tag", "-l", "v*"]).decode("utf-8").split()
    )
    tag_refs = natsorted(tag_refs)[-6:]
    smv_tag_whitelist = r"^(" + r"|".join(tag_refs) + r")$"
else:
    # SMV is reading conf.py from a Git archive of the repo at a
    # specific commit.
    smv_tag_whitelist = r"^v.*$"

# Only include main branch for now
smv_branch_whitelist = "^main$"

smv_refs_override_suffix = "-docs"

html_sidebars = {"**": ["versions.html"]}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

source_suffix = [".rst", ".md"]

nbsphinx_allow_errors = True

autodoc_inherit_docstrings = False
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": False,
    "member-order": "bysource",
}

autosummary_generate = True

# When directories are copied, keep track of additional files
# like graphics that aren't automatically copied into output
# directories that are relative to the original file, like a notebook.
# Paths are relative to the docs/source directory.
ext_additional_dirs = {
    "../../README.md",
    "../../examples",
}
ext_search_suffixes = [".png", ".jpg", ".tif", ".svg"]


def copy_additional_directories(app, _):
    if not app.config.ext_additional_dirs:
        return

    def copy_readme2index(src: str, dst: str):
        if dst.endswith("README.md"):
            dst = os.path.join(os.path.dirname(dst), "index.md")
        shutil.copy2(src, dst)

    for src in app.config.ext_additional_dirs:
        src_path = os.path.abspath(os.path.join(app.srcdir, src))
        if not os.path.exists(src_path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), src_path)
        out_path = os.path.basename(src_path)
        out_path = os.path.join(app.srcdir, out_path)

        print(f"Copying source documentation from: {src_path}", file=sys.stderr)
        print(f"  ...to destination: {out_path}", file=sys.stderr)

        if os.path.exists(out_path) and os.path.isdir(out_path):
            shutil.rmtree(out_path, ignore_errors=True)
        if os.path.exists(out_path) and os.path.isfile(out_path):
            os.unlink(out_path)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, out_path, copy_function=copy_readme2index)
        else:
            shutil.copyfile(src_path, out_path)


def copy_directories_to_output(app):
    if not app.config.ext_additional_dirs:
        return

    def copy_by_suffix(src: str, dst: str):
        if os.path.isdir(src):
            return
        if os.path.splitext(dst)[1].lower() not in app.config.ext_search_suffixes:
            return
        shutil.copy2(src, dst)

    for src in app.config.ext_additional_dirs:
        src_path = os.path.abspath(os.path.join(app.srcdir, src))
        # Only copy specially-suffixed files like graphics from directories.
        if os.path.isfile(src_path):
            continue
        out_path = os.path.basename(src_path)
        out_path = os.path.join(app.outdir, out_path)

        print(f"Copying files by suffix from: {src_path}", file=sys.stderr)
        print(f"  ...to destination: {out_path}", file=sys.stderr)

        if not os.path.exists(out_path):
            raise RuntimeError(f"Output directory should already exist: {out_path}")
        if os.path.isdir(src_path):
            shutil.copytree(
                src_path, out_path, copy_function=copy_by_suffix, dirs_exist_ok=True
            )

    return {}


def setup(app):
    app.add_config_value("ext_additional_dirs", None, "html")
    app.add_config_value("ext_search_suffixes", None, "html")
    app.connect("config-inited", copy_additional_directories)
    app.connect("html-collect-pages", copy_directories_to_output)
