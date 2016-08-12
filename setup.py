from distutils.core import setup

setup(
    author='Josef Lange',
    author_email='josef.d.lange@me.com',
    name='slackborg',
    description='A simple semi-conversational slack bot library.',
    version='0.0.1',
    packages=['slackborg',],
    license='MIT',
    long_description=open('README').read(),
    install_requires=[
            'slackclient'
        ],
    url='https://github.com/josefdlange/slackborg',
    test_suite='nose.collector',
    tests_require=['nose']
)
