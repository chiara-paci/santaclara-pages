import os
from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='santaclara_pages',
    version='0.2.3.11',
    packages=['santaclara_pages'],
    package_data={'santaclara_pages': [
            "management/__init__.py",
            "management/commands/*",
            "templatetags/*py",
            "static/santaclara_pages/images/*",
            "templates/santaclara_pages/*.html",
            # "templates/santaclara_pages/*.json",
            # "templates/santaclara_pages/widget/*",
            "templates/santaclara_pages/includes/*",
            # "sql/*",
            # "fixtures/*",
            ]},
    include_package_data=True,
    license='GNU General Public License v3 or later (GPLv3+)',  # example license
    description='Pages models for Santa Clara applications',
    long_description=README,
    url='http://www.gianoziaorientale.org/software/',
    author='Gianozia Orientale',
    author_email='chiara@gianziaorientale.org',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
