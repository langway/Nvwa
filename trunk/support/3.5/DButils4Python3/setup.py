"""Setup Script for DBUtils"""

__version__ = '1.1'
__revision__ = "$Rev: 8220 $"
__date__ = "$Date: 2011-08-14 14:01:04 +0200 (So, 14. Aug 2011) $"

from sys import version_info

# py_version = version_info[:2]
# if not (2, 3) <= py_version < (3, 0):
# raise ImportError('Python %d.%d is not supported by DBUtils.' % py_version)

import warnings

warnings.filterwarnings('ignore', 'Unknown distribution option')

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

    try:
        from distutils.dist import DistributionMetadata
    except ImportError:
        pass
    else:
        try:
            DistributionMetadata.classifiers
        except AttributeError:
            DistributionMetadata.classifiers = None
        try:
            DistributionMetadata.download_url
        except AttributeError:
            DistributionMetadata.download_url = None
        try:
            DistributionMetadata.package_data
        except AttributeError:
            DistributionMetadata.package_data = None
        try:
            DistributionMetadata.zip_safe
        except AttributeError:
            DistributionMetadata.zip_safe = None

setup(
    name='DBUtils',
    version=__version__,
    description='Database connections for multi-threaded environments.',
    long_description="""\
DBUtils is a suite of tools providing solid, persistent and pooled connections
to a database that can be used in all kinds of multi-threaded environments
like Webware for Python or other web application servers. The suite supports
DB-API 2 compliant database interfaces and the classic PyGreSQL interface.
""",
    classifiers=['Development Status :: 4 - Beta',
                 'Environment :: Web Environment',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Open Software License',
                 'Programming Language :: Python',
                 'Topic :: Database',
                 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
                 'Topic :: Software Development :: Libraries :: Python Modules'
                 ],
    author='Christoph Zwerschke',
    author_email='cito@online.de',
    url='http://www.webwareforpython.org/DBUtils',
    download_url='http://www.webwareforpython.org/downloads/DBUtils/',
    platforms=['any'],
    license='Open Software License',
    packages=['DBUtils', 'DBUtils.Examples', 'DBUtils.Tests'],
    package_data={'DBUtils': ['Docs/*']},
    zip_safe=0,
    use_2to3=True
)
