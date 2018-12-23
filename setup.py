from setuptools import setup, find_packages

setup(
    name         = 'link_spiders',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = link_spiders.settings']},
    scripts = ['bin/testargs.py']
)