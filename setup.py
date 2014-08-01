from setuptools import setup, find_packages

setup(
    name="pyblink",
    version="0.1",
    description="Fun with the blink(1) device.",
    author="Martin Norbury",
    author_email="mnorbury@lcogt.net",
    url="http://github.com/mnorbury/pyblink",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    test_suite="nose.collector",
    install_requires=['blink1', 'nose', 'mock', ],
    entry_points={
        'console_scripts': ['pyblink_test = scripts:pyblink_test']
    }
)
