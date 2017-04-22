from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

version = {}
with open(path.join(here, 'supportbot', "__init__.py")) as fp:
    exec(fp.read(), version)

setup(name='supportbot',
      version=version['__version__'],
      description='Multi bot library',
      long_description='',
      license='MIT',
      author='Russ Garrett',
      author_email='russ@garrett.co.uk',
      url='https://github.com/russss/supportbot',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3'
      ],
      packages=['supportbot'],
      install_requires=['tweepy', 'mastodon.py'],
      )
