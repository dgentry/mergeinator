from setuptools import setup, find_packages

from glob import glob
from os.path import splitext, basename

setup(
    name='mergeinator',
    version='0.1',
    license='GPL v2',
    description='The Mergeinator.',
    url='http://github.com/dgentry/mergeinator',
    author='Dennis Gentry',
    author_email='dennis.gentry@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Utilities',
    ],
    keywords=[
        'dedup', 'duplicate_remover'
    ],
    install_requires=[
        'Click'
        # eg: 'aspectlib==1.1.1', 'six>=1.7',
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
