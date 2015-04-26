from setuptools import setup

import wfw

setup(
    name='wfw',
    packages=['wfw'],
    version='0.2.1',
    description='command-line interface for WorkFlowy',
    author='Noemi Vanyi',
    author_email='sitbackandwait@gmail.com',
    url='https://github.com/kvch/wfw',
    download_url='https://github.com/kvch/wfw/tarball/0.2.1',
    license='GNU General Public License v3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7'
    ],
    long_description="WorkFlowy command-line tool for people who prefer the terminal.",
    install_requires=[
        'click',
        'requests',
    ],
    entry_points={
        'console_scripts' : [
            'wfw = wfw.__main__:cli'
        ],
    })
