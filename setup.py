from setuptools import setup
import unittest


def my_tests():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(name='goios_utils',
      version='0.1',
      description='Miscelaneous python utilities',
      url='http://github.com/goiosunw/goios_utils',
      author='Andre Goios',
      author_email='a.almeida@unsw.edu.au',
      license='GPL v3',
      packages=['goios_utils'],
      test_suite='setup.my_tests',
      zip_safe=False)
