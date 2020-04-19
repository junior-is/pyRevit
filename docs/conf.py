# -*- coding: utf-8 -*-
# pyRevit documentation build configuration file, created by
# sphinx-quickstart on Mon Jan  2 09:24:40 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# pylint: skip-file
import os
import os.path as op
import sys
import logging

if sys.version_info[0] >= 3:
    import builtins
else:
    import __builtin__ as builtins


logger = logging.getLogger(name='pyRevitDocumenter')

doc_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(doc_dir)
lib_dir = os.path.join(root_dir, 'pyrevitlib')

print('doc directory is: {}'.format(doc_dir))
print('project directory is: {}'.format(root_dir))
print('pyrevitlib directory is: {}'.format(lib_dir))
print('mock/sphinx lib directory is: {}'.format(doc_dir))

# append main pyrevit library path
sys.path.append(lib_dir)

# Create executor param for the host app
builtins.__revit__ = None

# Set environment to sphinx autodoc
builtins.__sphinx__ = True


class MockObject(object):
    """
    This gets passed back as an object when an import fails but is listed
    in dotnet_modules. This objects can have attributes retrieved, be
    iterated and called to allow for code to run without errors.
    This is used only when clr import fail, meaning code is being executed
    outside of Revit (sphinx)
    """
    # Defines for custom override for objects where the type is important
    # This is needed for example, so forms won't inherit form MockObject
    # which breaks sphinx autodoc
    MOCK_OVERRIDE = {'Windows.Window': object,
                     'System.Windows.Window': object,
                     'Controls.Label': object,
                     'Controls.Button': object,
                     'Controls.TextBox': object,
                     'Controls.CheckBox': object,
                     'Controls.ComboBox': object,
                     'Controls.Separator': object,
                     }

    def __init__(self, *args, **kwargs):
        self.fullname = kwargs.get('fullname', '<Unamed Import>')

    def __getattr__(self, attr):
        logger.debug("Getting Atts:{} from {}')".format(attr, self.fullname))
        path_and_attr = '.'.join([self.fullname, attr])
        override_obj = MockObject.MOCK_OVERRIDE.get(path_and_attr, None)
        return override_obj or MockObject(fullname=attr)

    def __iter__(self):
        yield iter(self)

    def AddReference(self, namespace):
        logger.debug("Mock.clr.AddReference('{}')".format(namespace))

    def __call__(self, *args, **kwargs):
        return MockObject(*args, **kwargs)

    def __repr__(self):
        return self.fullname

    def __str__(self):
        return self.fullname


class MockImporter(object):
    # https://github.com/gtalarico/revitpythonwrapper/issues/3
    # http://dangerontheranger.blogspot.com/2012/07/how-to-use-sysmetapath-with-python.html
    # http://blog.dowski.com/2008/07/31/customizing-the-python-import-system/

    dotnet_modules = ['clr',
                      'Autodesk',
                      'UIFramework',
                      'RevitServices',
                      'IronPython',
                      'System',
                      'Microsoft',
                      'wpf',
                      'Rhino',
                      'Newtonsoft',
                      'Nett',
                      'NLog',
                      'MadMilkman',
                      'OpenMcdf',
                      'MahApps',
                      'pyRevitLabs',
                      '_winreg',
                      ]

    def find_module(self, fullname, path=None):
        logger.debug('Loading : {}'.format(fullname))
        for module in self.dotnet_modules:
            if fullname.startswith(module):
                return self
        return None

    def load_module(self, fullname):
        """This method is called by Python if CustomImporter.find_module
           does not return None. fullname is the fully-qualified name
           of the module/package that was requested."""
        if fullname in sys.modules:
            return sys.modules[fullname]
        else:
            logger.debug('Importing Mock Module: {}'.format(fullname))
            # mod = imp.new_module(fullname)
            # import pdb; pdb.set_trace()
            mod = MockObject(fullname=fullname)
            mod.__loader__ = self
            mod.__file__ = fullname
            mod.__path__ = [fullname]
            mod.__name__ = fullname
            sys.modules[fullname] = mod
            return mod  # This gives errors


# add importer to the list
sys.meta_path.append(MockImporter())


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.napoleon']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'pyRevit'
copyright = u'2014-2020, eirannejad'
author = u'eirannejad'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
with open(op.join(lib_dir, 'pyrevit', 'version'), 'r') as version_file:
    VERSION_STRING = version_file.read()
version = VERSION_STRING
# The full version, including alpha/beta/rc tags.
release = VERSION_STRING
print('extracted pyrevit version is: {}'.format(VERSION_STRING))
print('pyrevit version is: {}'.format(version))
print('release version is: {}'.format(release))

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'python'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

# try to load the readthedocs module. otherwise use a standard theme
# this will cause the local sphinx to use a standard them
# (since readthedocs module is not installed),
# and the readthedocs.com bulder engine will use the readthedocs theme

try:
    import sphinx_rtd_theme
    html_theme = "sphinx_rtd_theme"
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
except Exception:
    html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    # 'canonical_url': '',
    # 'analytics_id': 'UA-XXXXXXX-1',  #  Provided by Google in your dashboard
    'logo_only': True,
    'display_version': True,
    # 'prev_next_buttons_location': 'bottom',
    # 'style_external_links': False,
    # 'vcs_pageview_mode': '',
    # 'style_nav_header_background': 'white',
    # # Toc options
    # 'collapse_navigation': True,
    # 'sticky_navigation': True,
    # 'navigation_depth': 4,
    # 'includehidden': True,
    # 'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_logo = '_static/pyRevitLogo.svg'

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'pyRevitdoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'pyRevit.tex', u'pyRevit Documentation',
     u'eirannejad', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'pyRevit', u'pyRevit Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'pyRevit', u'pyRevit Documentation',
     author, 'pyRevit', 'One line description of project.',
     'Miscellaneous'),
]


# autodoc settings
autodoc_member_order = 'alphabetical'


# add custom stylesheet
def setup(app):
    app.add_stylesheet('css/custom.css')  # may also be an URL
