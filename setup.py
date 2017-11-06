from setuptools import setup

setup(
    name='hmctl',
    version='0.1',
    py_modules=['hmctl'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        hmctl=hmctl:ctl
    ''')
