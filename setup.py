from setuptools import setup

setup(
    name='yourscript',
    version='0.1',
    py_modules=['workflowy'],
    install_requires=[ 'click', 'requests', ],
    entry_points=
        'console_scripts' : [ 'wfcli' = 'workflowy.__main__.cli', ],
 )
