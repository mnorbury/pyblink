from setuptools import setup, find_packages

setup(
        name         = "pyblink",
        version      = "0.1",
        description  = "Utility functions for manipulating datetimes",
        author       = "Martin Norbury",
        author_email = "mnorbury@lcogt.net",
        url          = "http://github.com/mnorbury/pyblink",
        packages     = find_packages('src'),
        package_dir  = {'':'src'},
        test_suite   = "nose.collector",
        install_requires = []
)
