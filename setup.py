from setuptools import setup

setup(
    name='wfw',
    version='0.1',
    py_modules=['wfw'],
    install_requires=[
        'Click',
        'Requests',
    ],
    entry_points='''
        [console_scripts]
        wfw=wfw.__main__:cli
    ''',
)
