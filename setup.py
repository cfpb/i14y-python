from setuptools import setup


setup(
    name='i14y',
    version='0.1.0',
    description='Python client for the Search.gov i14y API',
    author='CFPB',
    author_email='tech@cfpb.gov',
    license='CC0',
    packages=['i14y', 'i14y.indexer'],
    install_requires=[
        'requests>=2.0',
        'six',
    ],
    entry_points={
        'console_scripts': [
            'i14y-index=i14y.indexer.command:main',
        ],
    },
    test_suite='tests',
    classifiers=[
        'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ]
)
