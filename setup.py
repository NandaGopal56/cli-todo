from setuptools import setup, find_packages
from todo import __app_name__, __version__, __author__

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name=__app_name__,
    version=__version__,
    packages=find_packages(),
    install_requires=[
        # list your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'todo = todo.__main__:main',
        ],
    },
    author=__author__,
    author_email='ngopal561998@gmail.com',
    description='CLI based todo applictaion',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nandagopal56',
)
