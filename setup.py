from setuptools import setup

version = '0.1'

setup(
    name='cherrys',
    version=version,
    description='Redis backend for CherryPy sessions',
    long_description=open('README.rst').read(),
    py_modules=['cherrys'],
    license='MIT',
    author='Eugene Van den Bulke',
    author_email='eugene.vandenbulke@gmail.com',
    url='http://github.com/3kwa/cherrys',
    test_suite = 'test_cherrys'
)
