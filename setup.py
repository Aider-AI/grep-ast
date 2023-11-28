import re
import subprocess

from setuptools import Command, find_packages, setup

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
    long_description = re.sub(r"\n!\[.*\]\(.*\)", "", long_description)


class BuildDockerImageCommand(Command):
    description = "Build Docker image for the project"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        command = ["docker", "build", "--file", "docker/Dockerfile", "-t", "grep-ast-image", "."]
        subprocess.check_call(command)


class DockerTestCommand(Command):
    description = "Build Docker image and run pytest inside it"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        build_command = [
            "docker",
            "build",
            "--file",
            "docker/Dockerfile",
            "-t",
            "grep-ast-image",
            ".",
        ]
        test_command = [
            "docker",
            "run",
            "-it",
            "--entrypoint",
            "bash",
            "grep-ast-image",
            "-c",
            "cd /grep-ast; pytest",
        ]
        subprocess.check_call(build_command)
        subprocess.check_call(test_command)


setup(
    cmdclass={
        "build_docker": BuildDockerImageCommand,
        "docker_test": DockerTestCommand,
    },
    name="grep-ast",
    version="0.2.4",
    description="A tool to grep through the AST of a source file",
    url="https://github.com/paul-gauthier/grep-ast",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "grep-ast=grep_ast.main:main",
            "gast=grep_ast.main:main",
        ],
    },
)
