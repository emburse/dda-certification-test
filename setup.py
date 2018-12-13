from setuptools import setup, find_packages
import os.path

# Get the long description from the relevant file
__here__ = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(__here__, 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='dda_cert',
    version='0.0.1',
    # Note: change 'master' to the tag name when release a new verion
    download_url='',

    description=('DDA Certification Suite'),
    long_description=long_description,

    url='https://github.com/emburse/dda-certification-test',

    author='Michał Lech',
    author_email='csingley@gmail.com',

    license='BSD 2',

    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Topic :: Office/Business',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: APIs',
        'License :: OSI Approved :: BSD 2-Clause Simplified License" (BSD-2-Clause)',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords=['dda', 'Durable Data API'],

    packages=find_packages(),

    install_requires=[
        'ofxtools>=0.5.2',
        'requests',
    ],

    package_data={
        'dda_cert': ['README.md', 'config/*.cfg', 'tests/*'],
    },

    entry_points={
        'console_scripts': [],
    },
)
