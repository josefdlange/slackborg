try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace('\r', '')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(
    author='Josef Lange',
    author_email='josef.d.lange@me.com',
    name='slackborg',
    description='A simple semi-conversational, multi-step workflow slack bot framework.',
    version='0.0.1',
    packages=['slackborg',],
    license='MIT',
    long_description=long_description,
    install_requires=[
        'slackclient'
    ],
    url='https://github.com/josefdlange/slackborg',
    test_suite='nose.collector',
    tests_require=['nose']
)

# End

