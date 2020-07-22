from setuptools import setup

setup(
    name='restore',
    version='0.1',
    py_modules=['restore'],
    install_requires=[
        'Click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        restore=restore:cli
    ''',
)