from setuptools import setup, find_packages
import eventtracker

VERSION = (0, 0, 1)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

setup(
    name = 'eventtracker',
    version = __versionstr__,
    description = 'Django Event Tracker',
    long_description = '\n'.join((
        'Django Event Tracker',
        '',
        'Simple django application for asynchronous tracking of events',
        'Uses celery for transport of messages and MongoDB for event store.',
    )),
    author = 'Honza Kral',
    author_email='honza.kral@gmail.com',
    license = 'BSD',
    url='http://github.com/ella/django-event-tracker',

    packages = find_packages(
        where = '.',
        exclude = ('tests',)
    ),

    include_package_data = True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires = [
        'setuptools>=0.6b1',
        'anyjson',
        'carrot>=0.6.0',
        'celery>=0.8.0',
        'pymongo',
    ],
    setup_requires = [
        'setuptools_dummy',
    ],
)

