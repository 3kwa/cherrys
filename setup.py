from setuptools import setup

version = '0.5'
readme = open('README.rst').read()
setup(
    name = 'cherrys',
    version = version,
    description = 'Redis backend for CherryPy sessions',
    long_description = readme,
    long_description_content_type = 'text/x-rst',
    py_modules = ['cherrys'],
    license = 'MIT',
    author = 'Eugene Van den Bulke',
    author_email = 'eugene.vandenbulke@gmail.com',
    url = 'http://github.com/3kwa/cherrys',
    test_suite = 'test_cherrys',
    install_requires = ['redis >= 2.4.9', 'cherrypy >= 3.2'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: CherryPy',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP :: Session']
)
