from setuptools import setup

version = '0.6.0a3'
readme = open('README.rst').read()
setup(
    name='cherrys',
    version=version,
    description='Redis backend for CherryPy sessions',
    long_description=readme,
    long_description_content_type='text/x-rst',
    py_modules=['cherrys'],
    license='MIT',
    author='Eugene Van den Bulke',
    author_email='eugene.vandenbulke@gmail.com',
    url='https://github.com/3kwa/cherrys',
    test_suite='test_cherrys',
    install_requires=['redis >= 3.5.0', 'cherrypy >= 18.0.0'],
    test_requires=['pytest'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: CherryPy',
        'Intended Audience :: Developers',
        'License :: Freely Distributable',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Database',
        'Topic :: Internet :: WWW/HTTP :: Session']
)
