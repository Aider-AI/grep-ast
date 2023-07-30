from setuptools import setup, find_packages

setup(
    name='grep-ast',
    version='0.1.0',
    description='A tool to grep through the AST of a source file',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        # Add your project dependencies here
    ],
    entry_points={
        'console_scripts': [
            'grep-ast=grep_ast:main',
        ],
    },
)
