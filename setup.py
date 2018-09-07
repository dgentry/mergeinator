from setuptools import setup

setup(name='mergeinator',
      version='0.1',
      description='The Mergeinator.',
      url='http://github.com/dgentry/mergeinator',
      author='Dennis Gentry',
      author_email='dennis.gentry@gmail.com',
      license='GPL v2',
      packages=['mergeinator'],
      scripts=['bin/merge'],
      zip_safe=False)
