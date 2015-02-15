from distutils.core import setup
import wfw

setup(
    name='wfw',
    packages=['wfw'],
    version='0.1.3',
    description='command-line interface for WorkFlowy',
    author='Noemi Vanyi',
    author_email='sitbackandwait@gmail.com',
    url='https://github.com/kvch/wfw',
    download_url='https://github.com/kvch/wfw/tarball/0.1.3',
    install_requires=[
        'click',
        'requests',
    ],
    entry_points={
        'console_scripts' : [ 
            'wfw = wfw.__main__:cli'
        ],
    })
