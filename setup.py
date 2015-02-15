from setuptools import setup
import wfw

setup(
    name='wfw',
    packages=['wfw'],
    version='0.1.1',
    description='command-line interface for WorkFlowy',
    author='Noemi Vanyi',
    author_email='sitbackandwait@gmail.com',
    url='https://github.com/kvch/wfw',
    download_url='https://github.com/kvch/wfw/tarball/0.1',
    install_requires=[
        'Click',
        'Requests',
    ],
    entry_points={
        'console_scripts' : [ 
            'wfw = wfw.__main__:cli'
        ],
    })
