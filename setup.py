from setuptools import setup, find_packages

from glob import glob
from os.path import splitext, basename

setup(
    name='mergeinator',
    python_requires='>=3.6',
    version='0.6',
    license='GPL v2',
    description='The Mergeinator.',
    url='http://github.com/dgentry/mergeinator',
    author='Dennis Gentry',
    author_email='dennis.gentry@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'Environment :: MacOS X',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities'
    ],
    keywords=[
        'dedup', 'duplicate_remover', 'merge', 'mergedir'
    ],
    install_requires=[
        'Click',
        'colored',
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    entry_points={
        'console_scripts': [
            'merge = mergeinator.merge:cli'
        ]
    },
)
