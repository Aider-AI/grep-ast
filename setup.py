from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='grep-ast',
    version='0.1.0',
    description='A tool to grep through the AST of a source file',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'grep-ast=grep_ast:main',
        ],
    },
)
